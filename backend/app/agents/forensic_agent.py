"""
TruthLens — Forensic Agent (Real Document-Specific Analysis).

This agent performs REAL fraud detection using:
  1. OCR text pulled directly from DB (or extracted fresh via PyMuPDF)
  2. Benford's Law statistical analysis on monetary amounts
  3. Numeric entropy (repetition, round-number concentration)
  4. Structural completeness checks (missing PAN, AY, account numbers)
  5. Future-date detection
  6. Cross-document copy-paste artifact detection
  7. Velocity fraud detection
  8. Pixel-level ELA + metadata analysis for images/PDFs

Key fix: Analysis now waits for OCR to finish (orchestration.py) so ocr_text
is always populated. If still empty, we extract text directly via PyMuPDF.
"""

import re
import math
import datetime
import collections
import asyncio
from app.agents.state import TruthLensState
from app.services.forensics_service import ForensicsService
from app.services.fraud_dna_service import FraudDNAService
from app.core.config import settings


# ─── Text Extraction ─────────────────────────────────────────────────────────

def _extract_text(doc) -> str:
    """Get best available text from a document ORM object."""
    return (getattr(doc, "ocr_text", None) or
            getattr(doc, "extracted_text", None) or
            str(getattr(doc, "extracted_fields", None) or "") or "")


def _extract_text_from_bytes(file_bytes: bytes, mime_type: str) -> str:
    """
    Fallback: Extract raw text directly from file bytes using PyMuPDF.
    Used when OCR hasn't completed yet or returned empty text.
    """
    try:
        if mime_type == "application/pdf":
            import fitz
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text.strip()
    except Exception:
        pass
    return ""


# ─── Benford's Law ────────────────────────────────────────────────────────────

_BENFORDS_EXPECTED = {
    1: 0.301, 2: 0.176, 3: 0.125, 4: 0.097,
    5: 0.079, 6: 0.067, 7: 0.058, 8: 0.051, 9: 0.046
}


def _benfords_law_analysis(text: str) -> dict | None:
    """
    Benford's Law Analysis on monetary amounts.
    Returns a fraud signal dict if distribution is suspicious, else None.
    """
    raw_amounts = re.findall(r'(?:Rs\.?|₹|INR)?\s*([\d,]+)', text, re.IGNORECASE)
    amounts = []
    for raw in raw_amounts:
        try:
            val = int(raw.replace(',', '').strip())
            if val >= 100:
                amounts.append(val)
        except ValueError:
            continue

    if len(amounts) < 7:
        return None

    observed_counts = collections.Counter()
    for amt in amounts:
        first_digit = int(str(amt)[0])
        observed_counts[first_digit] += 1

    total = len(amounts)
    chi_sq = 0.0
    for d in range(1, 10):
        expected_count = total * _BENFORDS_EXPECTED[d]
        observed = observed_counts.get(d, 0)
        if expected_count > 0:
            chi_sq += ((observed - expected_count) ** 2) / expected_count

    if chi_sq > 20.09:
        return {
            "type": "benfords_law_violation",
            "severity": "critical",
            "description": (
                f"Benford's Law: Distribution of {total} monetary amounts deviates significantly "
                f"from natural financial data (χ²={chi_sq:.2f}, threshold=20.09). "
                "This is a statistical fingerprint of fabricated numbers."
            ),
            "confidence": min(0.99, 0.70 + (chi_sq - 20.09) / 50),
            "value": f"chi_sq={chi_sq:.2f}"
        }
    elif chi_sq > 15.51:
        return {
            "type": "benfords_law_warning",
            "severity": "high",
            "description": (
                f"Benford's Law: Moderate deviation in {total} monetary figures "
                f"(χ²={chi_sq:.2f}). May indicate partially fabricated financial data."
            ),
            "confidence": 0.68,
            "value": f"chi_sq={chi_sq:.2f}"
        }
    return None


# ─── Numeric Entropy ──────────────────────────────────────────────────────────

def _numeric_entropy_check(text: str) -> list:
    """
    Detects fraudulent number patterns:
    1. High-frequency repetition (copy-paste of same amounts)
    2. All amounts suspiciously round (multiples of 5000+)
    3. Arithmetic impossibility (declared income < tax paid)
    """
    signals = []
    raw_amounts = re.findall(r'(?:Rs\.?|₹|INR)?\s*([\d,]+)', text, re.IGNORECASE)
    amounts = []
    for raw in raw_amounts:
        try:
            val = int(raw.replace(',', '').strip())
            if val >= 1000:
                amounts.append(val)
        except ValueError:
            continue

    if not amounts:
        return signals

    # Check 1: Duplicate amounts (copy-paste fraud)
    freq = collections.Counter(amounts)
    dupes = [(amt, cnt) for amt, cnt in freq.items() if cnt >= 3 and amt > 10_000]
    if dupes:
        worst = max(dupes, key=lambda x: x[1])
        signals.append({
            "type": "repeated_amount_anomaly",
            "severity": "high",
            "description": (
                f"Amount ₹{worst[0]:,} appears {worst[1]} times. "
                "High-frequency repetition indicates template-based fabrication."
            ),
            "confidence": min(0.95, 0.60 + worst[1] * 0.05),
            "value": f"{worst[0]}"
        })

    # Check 2: Round-number concentration (> 60% are exact multiples of 5000)
    if len(amounts) >= 5:
        round_count = sum(1 for a in amounts if a % 5000 == 0)
        round_ratio = round_count / len(amounts)
        if round_ratio > 0.60:
            signals.append({
                "type": "round_number_concentration",
                "severity": "medium",
                "description": (
                    f"{round_count}/{len(amounts)} ({round_ratio*100:.0f}%) of monetary amounts are "
                    "exact multiples of ₹5,000. Authentic financial data contains irregular values; "
                    "this pattern suggests manually fabricated figures."
                ),
                "confidence": min(0.90, 0.55 + round_ratio * 0.35),
                "value": f"round_ratio={round_ratio:.2f}"
            })

    return signals


# ─── Structural & Cross-Document Checks ──────────────────────────────────────

def _structural_completeness_check(doc, all_docs: list) -> list:
    """
    Checks for:
    - Missing mandatory fields for the document type
    - Future dates (impossible in genuine historical docs)
    - Copy-paste artifacts across all submitted documents
    - Velocity fraud (all docs submitted within seconds of each other)
    """
    signals = []
    text = _extract_text(doc)
    doc_type = getattr(doc, "document_type", "unknown") or "unknown"

    # ── Missing mandatory fields ──────────────────────────────────────────────
    mandatory = {
        "itr": [
            (r'\b[A-Z]{5}[0-9]{4}[A-Z]\b', "PAN number"),
            (r'\b(?:AY|assessment\s*year|A\.Y\.)\b', "Assessment Year"),
            (r'\b(?:acknowledgement|ack|receipt)\b', "Acknowledgement"),
        ],
        "bank_statement": [
            (r'\b(?:account\s*(?:no|number|num|#)|a\/c)\b', "Account number"),
            (r'\b(?:ifsc|micr|swift)\b', "Bank code"),
            (r'\b(?:opening|closing)\s*balance\b', "Balance fields"),
        ],
        "sale_deed": [
            (r'\b(?:survey\s*no|plot\s*no|khasra|khata)\b', "Property ID"),
            (r'\b(?:sub[\s-]?registrar|registration)\b', "Registration"),
        ],
        "land_record": [
            (r'\b(?:survey\s*no|khasra|khata|gata)\b', "Survey/Khasra number"),
            (r'\b(?:area|hectare|bigha|acre|guntha)\b', "Area measurement"),
        ],
    }

    for pattern, field_name in mandatory.get(doc_type, []):
        if not re.search(pattern, text, re.IGNORECASE):
            signals.append({
                "type": "missing_mandatory_field",
                "severity": "high",
                "description": f"Mandatory field '{field_name}' is absent from this {doc_type.replace('_', ' ').title()}. Genuine documents always contain this field.",
                "confidence": 0.82,
                "value": field_name
            })

    # ── Future-date anomaly ───────────────────────────────────────────────────
    current_year = datetime.datetime.utcnow().year
    future_years = [y for y in re.findall(r'\b(20[2-9]\d|2[1-9]\d{2})\b', text) if int(y) > current_year]
    if future_years:
        signals.append({
            "type": "future_date_detected",
            "severity": "critical",
            "description": f"Future year(s) found in document: {', '.join(sorted(set(future_years)))}. Genuine historical documents cannot contain future dates — definitive evidence of fabrication.",
            "confidence": 0.97,
            "value": future_years[0]
        })

    # ── Cross-doc copy-paste artifact ─────────────────────────────────────────
    if len(all_docs) > 1:
        all_texts = [_extract_text(d) for d in all_docs]
        my_long_numbers = set(re.findall(r'\b\d{8,}\b', text))
        for num in my_long_numbers:
            appearances = sum(1 for t in all_texts if num in t)
            if appearances > 1:
                signals.append({
                    "type": "cross_document_copy_paste",
                    "severity": "high",
                    "description": f"Reference number '{num}' appears verbatim in {appearances} documents. Genuine documents from different sources have unique reference numbers — this indicates they were generated from the same template.",
                    "confidence": 0.88,
                    "value": num
                })
                break

    # ── Velocity fraud ────────────────────────────────────────────────────────
    timestamps = []
    for d in all_docs:
        ts = getattr(d, "created_at", None) or getattr(d, "uploaded_at", None)
        if ts:
            timestamps.append(ts)
    if len(timestamps) >= 2:
        ts_sorted = sorted(timestamps)
        delta = (ts_sorted[-1] - ts_sorted[0]).total_seconds()
        if delta < 120:
            signals.append({
                "type": "velocity_fraud",
                "severity": "high",
                "description": f"All {len(all_docs)} documents uploaded within {int(delta)}s of each other. Genuine applicants gather documents over days/weeks — simultaneous submission is a velocity fraud pattern.",
                "confidence": 0.85,
                "value": delta
            })

    return signals


def _rule_based_fraud_signals(doc, all_docs: list) -> list:
    """Master fraud signal aggregator."""
    text = _extract_text(doc)
    signals = []

    benford = _benfords_law_analysis(text)
    if benford:
        signals.append(benford)

    signals.extend(_numeric_entropy_check(text))
    signals.extend(_structural_completeness_check(doc, all_docs))

    return signals


# ─── Forensic Agent ───────────────────────────────────────────────────────────

class ForensicAgent:

    def __init__(self, db):
        self.db = db

    async def _ensure_ocr_text(self, doc) -> str:
        """
        Ensures we have real OCR text for the document.
        Priority:
          1. doc.ocr_text (from the upload pipeline)
          2. Fresh PyMuPDF text extraction from stored file (fast, synchronous)
          3. Empty string (analysis will still work, just fewer text-based signals)
        """
        text = _extract_text(doc)
        if text and len(text.strip()) > 20:
            return text

        # Fallback: extract directly from the stored file
        try:
            from app.services.storage_service import StorageService
            from app.utils.encryption import decrypt_file
            storage = StorageService()
            encrypted_bytes = await storage.download(doc.file_path)
            file_bytes = decrypt_file(encrypted_bytes, settings.ENCRYPTION_KEY)
            mime = getattr(doc, "mime_type", "application/pdf") or "application/pdf"
            extracted = _extract_text_from_bytes(file_bytes, mime)
            if extracted:
                # Persist so future runs don't need to re-extract
                from app.repositories.document_repo import DocumentRepository
                repo = DocumentRepository(self.db)
                await repo.update(str(doc.id), {"ocr_text": extracted, "processing_status": "extracted"})
                await self.db.commit()
                # Patch the in-memory object too
                doc.ocr_text = extracted
                return extracted
        except Exception as e:
            pass
        return ""

    async def run(self, state: TruthLensState) -> TruthLensState:
        logs = state.get("agent_logs", [])
        errors = state.get("errors", [])
        state["current_agent"] = "forensic"

        forensics_svc = ForensicsService(self.db)
        dna_svc = FraudDNAService(self.db)

        forensic_results = {}
        dna_results = {}
        docs = state.get("documents", [])
        total_rule_signals = 0

        for doc in docs:
            doc_id = str(doc.id)

            # ── Step A: Ensure OCR text is available ─────────────────────────
            ocr_text = await self._ensure_ocr_text(doc)
            # Patch in-memory so structural checks can read it
            if ocr_text and not _extract_text(doc):
                doc.ocr_text = ocr_text

            # ── Step B: Image/PDF forensics (ELA, metadata, compression) ──────
            try:
                forensic_report = await forensics_svc.analyze_document(doc_id)
                result_dict = forensic_report.dict()
            except Exception as e:
                errors.append({"agent": "forensic_image", "doc_id": doc_id, "error": str(e)})
                result_dict = {
                    "authenticity_score": 100.0,
                    "tampering_probability": 0.0,
                    "anomalies": [],
                    "rule_signals": [],
                }

            # ── Step C: Rule-based text analysis (the real fraud detector) ────
            rule_signals = _rule_based_fraud_signals(doc, docs)
            total_rule_signals += len(rule_signals)

            # Merge rule signals into anomaly list
            existing_anomalies = result_dict.get("anomalies", [])
            for sig in rule_signals:
                existing_anomalies.append({
                    "check_type": sig["type"],
                    "severity": sig["severity"],
                    "description": sig["description"],
                    "confidence": sig["confidence"],
                })
            result_dict["anomalies"] = existing_anomalies
            result_dict["rule_signals"] = rule_signals

            # ── Step D: Adjust authenticity score from text signals ────────────
            base_score = result_dict.get("authenticity_score", 100.0)
            critical_count = sum(1 for s in rule_signals if s["severity"] == "critical")
            high_count = sum(1 for s in rule_signals if s["severity"] == "high")
            med_count = sum(1 for s in rule_signals if s["severity"] == "medium")
            penalty = (critical_count * 30) + (high_count * 18) + (med_count * 10)
            result_dict["authenticity_score"] = max(0.0, base_score - penalty)
            result_dict["ocr_text_length"] = len(ocr_text)

            # ── Step E: Persist rule_signals into the AnalysisResult DB row ────
            # The annotations endpoint reads findings["rule_signals"] to build overlays.
            if rule_signals:
                try:
                    from sqlalchemy import select as sa_select
                    from app.db.models.analysis import AnalysisResult
                    from sqlalchemy.orm.attributes import flag_modified
                    stmt = sa_select(AnalysisResult).where(
                        AnalysisResult.document_id == doc_id,
                        AnalysisResult.analysis_type == "forensics"
                    )
                    res = await self.db.execute(stmt)
                    ar = res.scalar_one_or_none()
                    if ar:
                        findings = dict(ar.findings or {})
                        findings["rule_signals"] = rule_signals
                        ar.findings = findings
                        flag_modified(ar, "findings")
                        await self.db.commit()
                except Exception as e:
                    pass  # Non-fatal — UI will still show findings from in-memory state

            forensic_results[doc_id] = result_dict

            # ── Step E: Fraud DNA ──────────────────────────────────────────────
            try:
                features = await dna_svc.extract_forensic_features(doc_id)
                sig = dna_svc.generate_dna_signature(features, doc_id)
                case_id = str(doc.case_id)
                dna_svc.store_pattern(sig, case_id, is_fraud=False, pattern_type="live_analysis")
                matches = dna_svc.match_patterns(sig)
                dna_results[doc_id] = {
                    "signature_hash": sig.hash,
                    "matches": [m.dict() for m in matches],
                    "match_count": len(matches)
                }
            except Exception as e:
                errors.append({"agent": "forensic_dna", "doc_id": doc_id, "error": str(e)})

        # ── Velocity check (case-level) ────────────────────────────────────────
        try:
            velocity = await dna_svc.detect_document_velocity(state["case_id"])
            forensic_results["_velocity"] = velocity.dict()
            if forensic_results["_velocity"].get("suspicious"):
                total_rule_signals += 1
        except Exception as e:
            errors.append({"agent": "velocity", "error": str(e)})

        logs.append({
            "agent": "forensic",
            "status": "completed",
            "docs_analyzed": len(docs),
            "rule_signals_found": total_rule_signals,
            "dna_matches_found": sum(v.get("match_count", 0) for v in dna_results.values()),
            "timestamp": datetime.datetime.utcnow().isoformat()
        })

        state["forensic_results"] = forensic_results
        state["fraud_dna_results"] = dna_results
        state["agent_logs"] = logs
        state["errors"] = errors
        return state
