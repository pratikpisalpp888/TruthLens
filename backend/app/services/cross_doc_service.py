"""
TruthLens — Cross-Document Consistency Engine.

Fix applied: When extracted_fields is empty (extractor pipeline not yet done),
we now fall back to regex-based field extraction from ocr_text directly.
This means cross-doc analysis always runs on real document data.
"""

import time
import re
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from thefuzz import fuzz

from app.db.models.document import Document
from app.repositories.document_repo import DocumentRepository
from app.repositories.analysis_repo import AnalysisResultRepository
from app.schemas.cross_doc import Mismatch, CrossDocReportResponse


def _ocr_extract_fields(doc: Document) -> dict:
    """
    Fallback field extractor using regex on ocr_text when extracted_fields is empty.
    Returns a best-effort dict of key fields.
    """
    fields = dict(doc.extracted_fields or {})
    if fields:
        return fields  # Already has structured data

    text = getattr(doc, "ocr_text", None) or ""
    if not text:
        return {}

    # PAN
    pan_m = re.search(r'\b([A-Z]{5}[0-9]{4}[A-Z])\b', text)
    if pan_m:
        fields["pan"] = pan_m.group(1)

    # Assessment Year (ITR)
    ay_m = re.search(r'\b(20\d{2}-\d{2})\b', text)
    if ay_m:
        fields["assessment_year"] = ay_m.group(1)

    # Name — look for lines after "Name of Assessee" or "Account Holder"
    name_m = re.search(
        r'(?:name\s+of\s+assessee|account\s+holder(?:\s+name)?|applicant\s+name)[:\s]+([A-Z][a-zA-Z\s]{3,40})',
        text, re.IGNORECASE
    )
    if name_m:
        fields["name_of_assessee"] = name_m.group(1).strip()

    # Gross Total Income (ITR)
    income_m = re.search(
        r'(?:gross\s+total\s+income|total\s+income|annual\s+income)[^\d]*([\d,]+)',
        text, re.IGNORECASE
    )
    if income_m:
        fields["gross_total_income"] = income_m.group(1).replace(",", "")

    # Account Number (bank statement)
    acc_m = re.search(r'(?:account\s+(?:no|number|num|#)|a\/c\s+no)[:\s.]*(\d{9,18})', text, re.IGNORECASE)
    if acc_m:
        fields["account_number"] = acc_m.group(1)

    # IFSC
    ifsc_m = re.search(r'\b([A-Z]{4}0[A-Z0-9]{6})\b', text)
    if ifsc_m:
        fields["ifsc"] = ifsc_m.group(1)

    # Total credits (bank statement) — sum of all credit amounts
    credits = re.findall(r'(?:cr|credit)[^\d]*([\d,]+)', text, re.IGNORECASE)
    if credits:
        total_cr = sum(int(c.replace(',', '')) for c in credits if c.replace(',', '').isdigit())
        if total_cr > 0:
            fields["total_credits"] = str(total_cr)

    # Survey number (sale deed / land record)
    survey_m = re.search(r'(?:survey\s+(?:no|number)|khasra\s+(?:no|number))[:\s]*([0-9A-Za-z/\-]+)', text, re.IGNORECASE)
    if survey_m:
        fields["survey_number"] = survey_m.group(1).strip()

    # Area
    area_m = re.search(r'(?:area|extent)[:\s]*([\d,.]+)\s*(?:sq|sqft|sqm|acre|hectare|bigha|guntha)?', text, re.IGNORECASE)
    if area_m:
        fields["area"] = area_m.group(1).replace(",", "")

    return fields


class CrossDocumentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.doc_repo = DocumentRepository(db)
        self.analysis_repo = AnalysisResultRepository(db)

    async def analyze_case(self, case_id: str) -> CrossDocReportResponse:
        start_time = time.time()

        docs = await self.doc_repo.get_by_case(case_id)

        # Use OCR fallback — so we always have fields even if extractor didn't finish
        enriched_docs = []
        for doc in docs:
            doc._ocr_fields = _ocr_extract_fields(doc)
            enriched_docs.append(doc)

        # Run all consistency checks
        identity_mismatches = self.check_identity_consistency(enriched_docs)
        property_mismatches = self.check_property_consistency(enriched_docs)
        financial_mismatches = self.check_financial_consistency(enriched_docs)
        timeline_mismatches = self.check_timeline_consistency(enriched_docs)

        all_mismatches = identity_mismatches + property_mismatches + financial_mismatches + timeline_mismatches

        score = self.calculate_consistency_score(all_mismatches)
        critical_findings = [m for m in all_mismatches if m.severity == "critical"]

        checks = {
            "identity": identity_mismatches,
            "property": property_mismatches,
            "financial": financial_mismatches,
            "timeline": timeline_mismatches
        }

        processing_time = int((time.time() - start_time) * 1000)

        # Save to DB
        await self.analysis_repo.create({
            "case_id": case_id,
            "analysis_type": "cross_document",
            "findings": {k: [m.dict(exclude_none=True) for m in v] for k, v in checks.items()},
            "score": score,
            "severity": "high" if score < 70 else "low",
            "confidence": 0.9,
            "processing_time_ms": processing_time
        })
        await self.db.commit()

        return CrossDocReportResponse(
            case_id=case_id,
            consistency_score=score,
            total_checks=len(enriched_docs) * 4,
            mismatches_found=len(all_mismatches),
            checks=checks,
            critical_findings=critical_findings,
            processing_time_ms=processing_time
        )

    def _get_fields(self, doc) -> dict:
        """Get fields from the enriched doc — prefers extracted_fields, falls back to OCR-derived."""
        return getattr(doc, "_ocr_fields", None) or doc.extracted_fields or {}

    def check_identity_consistency(self, docs: List[Document]) -> List[Mismatch]:
        mismatches = []
        names = {}
        pans = {}

        for doc in docs:
            fields = self._get_fields(doc)
            doc_type = doc.document_type or "unknown"

            name = (fields.get("name_of_assessee") or fields.get("vendee_name") or
                    fields.get("account_holder_name") or fields.get("owner_name") or
                    fields.get("applicant_name"))
            if name:
                names[doc_type] = name.strip()

            pan = fields.get("pan") or fields.get("pan_number")
            if pan:
                pans[doc_type] = pan.strip().upper()

        # Compare names across document types
        doc_types = list(names.keys())
        for i in range(len(doc_types)):
            for j in range(i + 1, len(doc_types)):
                t1, t2 = doc_types[i], doc_types[j]
                n1, n2 = names[t1], names[t2]
                score = fuzz.token_sort_ratio(n1, n2)
                if score < 85:
                    severity = "warning" if score >= 60 else "critical"
                    mismatches.append(Mismatch(
                        field="applicant_name",
                        type="identity",
                        severity=severity,
                        values={t1: n1, t2: n2},
                        similarity_scores={f"{t1}_vs_{t2}": score},
                        assessment=f"Name mismatch between {t1} and {t2} (similarity: {score}%). This could indicate identity fraud or document substitution."
                    ))

        # Compare PANs (must be exact match)
        pan_types = list(pans.keys())
        for i in range(len(pan_types)):
            for j in range(i + 1, len(pan_types)):
                t1, t2 = pan_types[i], pan_types[j]
                p1, p2 = pans[t1], pans[t2]
                if p1 != p2:
                    mismatches.append(Mismatch(
                        field="pan_number",
                        type="identity",
                        severity="critical",
                        values={t1: p1, t2: p2},
                        assessment=f"PAN mismatch: {p1} (from {t1}) ≠ {p2} (from {t2}). PAN must be identical across all documents — this is a critical fraud signal."
                    ))

        return mismatches

    def _extract_number(self, text: str) -> float:
        if not text:
            return 0.0
        clean = re.sub(r'[^\d\.]', '', str(text))
        try:
            return float(clean)
        except ValueError:
            return 0.0

    def check_property_consistency(self, docs: List[Document]) -> List[Mismatch]:
        mismatches = []
        sale_deeds = [d for d in docs if d.document_type == "sale_deed"]
        land_records = [d for d in docs if d.document_type == "land_record"]

        if not sale_deeds or not land_records:
            return mismatches

        sd = self._get_fields(sale_deeds[0])
        lr = self._get_fields(land_records[0])

        # Compare Survey Numbers
        sd_sy = sd.get("survey_number", "")
        lr_sy = lr.get("survey_number", "")
        if sd_sy and lr_sy and sd_sy.strip() != lr_sy.strip():
            mismatches.append(Mismatch(
                field="survey_number",
                type="property",
                severity="critical",
                values={"sale_deed": sd_sy, "land_record": lr_sy},
                assessment="Survey numbers do not match between Sale Deed and Land Record. This could indicate a different property is being used as collateral."
            ))

        # Compare Area
        sd_area = self._extract_number(sd.get("area", ""))
        lr_area = self._extract_number(lr.get("area", ""))
        if sd_area > 0 and lr_area > 0:
            dev = abs(sd_area - lr_area) / max(sd_area, lr_area) * 100
            if dev >= 5:
                severity = "low"
                if dev >= 50:
                    severity = "critical"
                elif dev >= 20:
                    severity = "high"
                elif dev >= 5:
                    severity = "medium"
                mismatches.append(Mismatch(
                    field="area",
                    type="property",
                    severity=severity,
                    values={"sale_deed": sd.get("area"), "land_record": lr.get("area")},
                    deviation_percent=round(dev, 2),
                    assessment=f"Property area discrepancy of {round(dev)}% between Sale Deed and Land Record."
                ))

        return mismatches

    def check_financial_consistency(self, docs: List[Document]) -> List[Mismatch]:
        mismatches = []
        itrs = [d for d in docs if d.document_type == "itr"]
        banks = [d for d in docs if d.document_type == "bank_statement"]

        if not itrs or not banks:
            return mismatches

        itr_fields = self._get_fields(itrs[0])
        bank_fields = self._get_fields(banks[0])

        itr_income = self._extract_number(itr_fields.get("gross_total_income", ""))
        bank_credits = self._extract_number(bank_fields.get("total_credits", "0"))

        if itr_income > 0 and bank_credits > 0:
            dev = abs(itr_income - bank_credits) / max(itr_income, bank_credits) * 100
            if dev > 30:
                severity = "critical" if dev > 100 else "high"
                mismatches.append(Mismatch(
                    field="annual_income",
                    type="financial",
                    severity=severity,
                    values={"itr_declared": itr_income, "bank_credits": bank_credits},
                    deviation_percent=round(dev, 2),
                    description=f"Bank credits (₹{bank_credits:,.0f}) deviate {round(dev)}% from ITR declared income (₹{itr_income:,.0f}). Income inflation is the most common loan fraud pattern."
                ))

        return mismatches

    def check_timeline_consistency(self, docs: List[Document]) -> List[Mismatch]:
        mismatches = []
        import datetime
        now = datetime.datetime.now()

        for doc in docs:
            if doc.document_type == "sale_deed":
                fields = self._get_fields(doc)
                reg_date_str = fields.get("registration_date")
                if reg_date_str:
                    try:
                        parts = re.split(r'[\/\-\.]', reg_date_str)
                        if len(parts) == 3:
                            if len(parts[2]) == 2:
                                parts[2] = "20" + parts[2]
                            dt = datetime.datetime(int(parts[2]), int(parts[1]), int(parts[0]))
                            if dt > now:
                                mismatches.append(Mismatch(
                                    field="registration_date",
                                    type="timeline",
                                    severity="critical",
                                    detail=f"Property registration date ({reg_date_str}) is in the future — this document is fabricated."
                                ))
                    except Exception:
                        pass
        return mismatches

    def calculate_consistency_score(self, mismatches: List[Mismatch]) -> float:
        score = 100.0
        for m in mismatches:
            if m.severity == "critical":
                score -= 25
            elif m.severity == "high":
                score -= 15
            elif m.severity in ("warning", "medium"):
                score -= 8
            elif m.severity == "low":
                score -= 3
        return max(0.0, score)
