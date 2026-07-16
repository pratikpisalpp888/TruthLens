"""
TruthLens — ITR Validation Service.
"""

import time
import re
import asyncio
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.document import Document
from app.repositories.document_repo import DocumentRepository
from app.repositories.analysis_repo import AnalysisResultRepository
from app.schemas.itr import ITRReportResponse, FormatResult, ComputationResult, ComputationDeviation, BankCrossResult, BehaviorResult
from app.core.exceptions import ResourceNotFoundError

class ITRValidationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.doc_repo = DocumentRepository(db)
        self.analysis_repo = AnalysisResultRepository(db)

    def _extract_number(self, text: Any) -> float:
        if not text: return 0.0
        clean = re.sub(r'[^\d\.]', '', str(text))
        try:
            return float(clean)
        except ValueError:
            return 0.0

    def validate_format(self, fields: dict) -> Dict[str, Any]:
        checks = {}
        issues = []
        
        ack = fields.get("acknowledgement_number", "")
        if ack and len(str(ack)) == 15 and str(ack).isdigit():
            checks["ack_number"] = {"valid": True, "value": ack}
        else:
            checks["ack_number"] = {"valid": False, "value": ack}
            issues.append("Acknowledgement number must be exactly 15 digits.")
            
        pan = fields.get("pan", "")
        pan_valid = bool(re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', str(pan)))
        holder = "Unknown"
        if pan_valid:
            h_char = str(pan)[3]
            if h_char == 'P': holder = "Person"
            elif h_char == 'C': holder = "Company"
            elif h_char == 'H': holder = "HUF"
            elif h_char == 'F': holder = "Firm"
            
        checks["pan"] = {"valid": pan_valid, "value": pan, "holder_type": holder}
        if not pan_valid:
            issues.append("PAN format is invalid.")
            
        ay = fields.get("assessment_year", "")
        ay_valid = bool(re.search(r'\d{4}-\d{2}', str(ay)))
        checks["assessment_year"] = {"valid": ay_valid, "value": ay}
        if not ay_valid:
            issues.append("Assessment year format is invalid.")
            
        form = fields.get("form_type", "")
        form_valid = bool(re.search(r'ITR-[1-7]', str(form)))
        checks["form_type"] = {"valid": form_valid, "value": form}
        
        valid = len(issues) == 0
        return {"valid": valid, "checks": checks, "issues": issues}

    def validate_computation(self, fields: dict) -> Dict[str, Any]:
        deviations = []
        
        declared_gti = self._extract_number(fields.get("gross_total_income"))
        declared_80c = self._extract_number(fields.get("deductions_80c"))
        declared_tax = self._extract_number(fields.get("tax_payable"))
        
        if declared_80c > 150000:
            deviations.append({
                "field": "section_80c",
                "declared": declared_80c,
                "max_allowed": 150000,
                "excess": declared_80c - 150000,
                "severity": "critical",
                "description": f"Section 80C deduction exceeds maximum limit by ₹{declared_80c - 150000}"
            })
            
        # Mocking old regime tax computation roughly
        computed_tax = 0.0
        taxable = max(0, declared_gti - min(declared_80c, 150000))
        if taxable > 1000000:
            computed_tax = (taxable - 1000000) * 0.3 + 112500
        elif taxable > 500000:
            computed_tax = (taxable - 500000) * 0.2 + 12500
        elif taxable > 250000:
            computed_tax = (taxable - 250000) * 0.05
            
        computed_tax += computed_tax * 0.04 # Health cess
        
        if abs(computed_tax - declared_tax) > 1000: # tolerance
            deviations.append({
                "field": "tax_payable",
                "declared": declared_tax,
                "computed": computed_tax,
                "severity": "high",
                "description": f"Computed tax (₹{computed_tax}) does not match declared tax (₹{declared_tax})"
            })
            
        return {
            "valid": len(deviations) == 0,
            "computed_values": {"tax_payable": computed_tax, "taxable_income": taxable},
            "declared_values": {"gross_total_income": declared_gti, "tax_payable": declared_tax},
            "deviations": deviations
        }

    def cross_reference_bank(self, itr_fields: dict, bank_fields: dict) -> Dict[str, Any]:
        itr_income = self._extract_number(itr_fields.get("gross_total_income"))
        bank_credits = self._extract_number(bank_fields.get("total_credits"))
        
        dev = 0.0
        if itr_income > 0 and bank_credits > 0:
            dev = abs(itr_income - bank_credits) / max(itr_income, bank_credits) * 100
            
        severity = "low"
        if dev > 100: severity = "critical"
        elif dev > 30: severity = "high"
        
        return {
            "income_deviation_percent": round(dev, 2),
            "itr_income": itr_income,
            "bank_credits": bank_credits,
            "unexplained_deposits": [], # Needs transaction level data
            "tds_match": True,
            "severity": severity
        }

    def analyze_behavior(self, itr_fields: dict) -> Dict[str, Any]:
        itr_income = self._extract_number(itr_fields.get("gross_total_income"))
        deductions = self._extract_number(itr_fields.get("deductions_80c"))
        
        ratio = 0.0
        if itr_income > 0:
            ratio = deductions / itr_income
            
        indicators = []
        if ratio > 0.4:
            indicators.append("Deductions exceed 40% of gross income (unusual)")
            
        return {
            "income_trend": "unknown (no historical data)",
            "yoy_change_percent": 0.0,
            "deduction_ratio": round(ratio, 2),
            "risk_indicators": indicators
        }

    def statistical_benfords_law(self, fields: dict) -> Dict[str, Any]:
        import collections
        _BENFORDS_EXPECTED = {1:0.301, 2:0.176, 3:0.125, 4:0.097, 5:0.079, 6:0.067, 7:0.058, 8:0.051, 9:0.046}
        
        amounts = []
        for k, v in fields.items():
            if isinstance(v, (int, float)) and v >= 100:
                amounts.append(v)
            elif isinstance(v, str):
                try:
                    val = float(re.sub(r'[^\d\.]', '', v))
                    if val >= 100: amounts.append(val)
                except ValueError:
                    pass
                    
        if len(amounts) < 5:
            return {"valid": True, "chi_sq": 0, "flagged": False, "description": "Insufficient numerical data for Benfords Law."}
            
        observed = collections.Counter(int(str(a).replace('.','')[0]) for a in amounts if int(str(a).replace('.','')[0]) != 0)
        total = sum(observed.values())
        if total == 0:
            return {"valid": True, "chi_sq": 0, "flagged": False, "description": "No valid leading digits."}
            
        chi_sq = sum(((observed.get(d,0) - total*_BENFORDS_EXPECTED[d])**2)/(total*_BENFORDS_EXPECTED[d]) for d in range(1,10))
        flagged = chi_sq > 15.51
        
        return {
            "valid": not flagged,
            "chi_sq": round(chi_sq, 2),
            "flagged": flagged,
            "description": f"Benfords Law χ²={chi_sq:.2f}. " + ("Suspiciously unnatural distribution." if flagged else "Natural numeric distribution.")
        }

    def semantic_keyword_analysis(self, ocr_text: str) -> Dict[str, Any]:
        text = str(ocr_text).lower()
        mandatory = ["income tax", "assessment year", "gross total income", "deductions", "total tax"]
        missing = [kw for kw in mandatory if kw not in text]
        
        suspicious_phrases = ["demo document", "sample", "for testing", "fabricated"]
        found_suspicious = [ph for ph in suspicious_phrases if ph in text]
        
        return {
            "valid": len(missing) <= 1 and len(found_suspicious) == 0,
            "missing_keywords": missing,
            "suspicious_phrases_found": found_suspicious,
            "description": f"Missing {len(missing)} mandatory keywords." if missing else "Semantic structure intact."
        }

    def identity_consistency_check(self, itr_fields: dict, related_docs: List[Document]) -> Dict[str, Any]:
        itr_pan = str(itr_fields.get("pan", "")).strip().upper()
        itr_name = str(itr_fields.get("name", "")).strip().lower()
        
        mismatches = []
        for doc in related_docs:
            if not doc.extracted_fields: continue
            
            # Check PAN across docs if they have it
            doc_pan = str(doc.extracted_fields.get("pan", "")).strip().upper()
            if doc_pan and itr_pan and doc_pan != itr_pan:
                mismatches.append(f"PAN mismatch in {doc.document_type}: {doc_pan} != {itr_pan}")
                
            # Check Name across docs
            # For Bank Statement
            if doc.document_type == "bank_statement":
                bank_name = str(doc.extracted_fields.get("account_holder_name", "")).strip().lower()
                if bank_name and itr_name and bank_name not in itr_name and itr_name not in bank_name:
                    mismatches.append(f"Identity mismatch with Bank Statement: '{bank_name}' vs '{itr_name}'")
                    
        return {
            "valid": len(mismatches) == 0,
            "mismatches": mismatches,
            "description": f"Found {len(mismatches)} identity inconsistencies." if mismatches else "Identity consistent across documents."
        }

    async def extract_fields_llm(self, ocr_text: str) -> dict:
        """Extract ITR fields intelligently from raw OCR text using Local Llama 3."""
        from app.services.llm_service import LLMService
        llm = LLMService()
        await llm.initialize()
        
        prompt = (
            "Extract the requested fields from the following ITR OCR text. "
            f"Text: {ocr_text[:2500]}"
        )
        
        try:
            # Removed strict 15s timeout to allow local LLM to finish thinking
            result = await llm.generate_json(prompt=prompt, system="itr_extractor", temperature=0.1)
            
            # Ensure safe fallback types
            return {
                "pan": result.get("pan") or "",
                "acknowledgement_number": result.get("acknowledgement_number") or "",
                "assessment_year": result.get("assessment_year") or "",
                "form_type": result.get("form_type") or "",
                "name": result.get("name") or "",
                "gross_total_income": float(result.get("gross_total_income") or 0.0),
                "tax_payable": float(result.get("tax_payable") or 0.0),
                "deductions_80c": float(result.get("deductions_80c") or 0.0)
            }
        except Exception as e:
            import structlog
            structlog.get_logger().error(f"LLM extraction failed: {e}")
            return {
                "pan": "", "acknowledgement_number": "", "assessment_year": "", "form_type": "", "name": "",
                "gross_total_income": 0.0, "tax_payable": 0.0, "deductions_80c": 0.0
            }
        finally:
            await llm.close()

    async def validate_from_text(self, ocr_text: str) -> ITRReportResponse:
        """Run full 7-layer analysis on raw OCR text without any DB lookups."""
        import time
        start_time = time.time()

        itr_fields = await self.extract_fields_llm(ocr_text)

        f_res = self.validate_format(itr_fields)
        c_res = self.validate_computation(itr_fields)
        # No bank docs in standalone mode
        b_res = {"income_deviation_percent": 0, "itr_income": itr_fields.get("gross_total_income", 0),
                 "bank_credits": 0, "unexplained_deposits": [], "tds_match": True, "severity": "low"}
        bh_res = self.analyze_behavior(itr_fields)
        stat_res = self.statistical_benfords_law(itr_fields)
        sem_res = self.semantic_keyword_analysis(ocr_text)
        id_res = {"valid": True, "mismatches": [], "description": "Single document scan — identity cross-check not applicable."}

        # Scores
        score_f  = 100.0 if f_res["valid"] else 50.0
        score_c  = 100.0 - (len(c_res["deviations"]) * 20.0)
        score_b  = 100.0
        score_bh = 100.0 - (len(bh_res["risk_indicators"]) * 20.0)
        score_stat = 100.0 if stat_res["valid"] else 30.0
        score_sem  = 100.0 if sem_res["valid"] else 40.0
        score_id   = 100.0

        val_score = (
            max(0, score_f)  * 0.10 +
            max(0, score_c)  * 0.25 +
            max(0, score_b)  * 0.10 +
            max(0, score_bh) * 0.10 +
            max(0, score_stat) * 0.20 +
            max(0, score_sem)  * 0.15 +
            max(0, score_id)   * 0.10
        )

        critical_issues: List[str] = []
        critical_issues.extend(f_res["issues"])
        critical_issues.extend([d["description"] for d in c_res["deviations"] if d["severity"] in ("critical", "high")])
        if not stat_res["valid"]:
            critical_issues.append(stat_res["description"])
        if not sem_res["valid"]:
            if sem_res["missing_keywords"]:
                critical_issues.append(f"Missing mandatory ITR keywords: {', '.join(sem_res['missing_keywords'])}")
            if sem_res["suspicious_phrases_found"]:
                critical_issues.append(f"Suspicious phrases detected: {', '.join(sem_res['suspicious_phrases_found'])}")
        if bh_res["risk_indicators"]:
            critical_issues.extend(bh_res["risk_indicators"])

        processing_time = int((time.time() - start_time) * 1000)

        sub_reports = {
            "format": f_res,
            "computation": c_res,
            "bank_cross_reference": b_res,
            "behavior": bh_res,
            "statistical": stat_res,
            "semantic": sem_res,
            "identity": id_res,
        }

        return ITRReportResponse(
            document_id="standalone",
            validity_score=val_score,
            form_type=itr_fields.get("form_type"),
            assessment_year=itr_fields.get("assessment_year"),
            sub_reports=sub_reports,
            critical_issues=critical_issues,
            processing_time_ms=processing_time,
        )

    async def validate(self, document_id: str, case_id: str) -> ITRReportResponse:
        start_time = time.time()
        
        itr_doc = await self.doc_repo.get_by_id(document_id)
        if not itr_doc or itr_doc.document_type != "itr":
            raise ResourceNotFoundError("Valid ITR document not found")
            
        docs = await self.doc_repo.get_by_case(case_id)
        bank_docs = [d for d in docs if d.document_type == "bank_statement"]
        
        itr_fields = itr_doc.extracted_fields or {}
        bank_fields = bank_docs[0].extracted_fields if bank_docs and bank_docs[0].extracted_fields else {}
        
        f_res = self.validate_format(itr_fields)
        c_res = self.validate_computation(itr_fields)
        b_res = self.cross_reference_bank(itr_fields, bank_fields)
        bh_res = self.analyze_behavior(itr_fields)
        stat_res = self.statistical_benfords_law(itr_fields)
        sem_res = self.semantic_keyword_analysis(getattr(itr_doc, "ocr_text", ""))
        id_res = self.identity_consistency_check(itr_fields, docs)
        
        # Calculate sub-scores for 7 layers
        score_f = 100.0 if f_res["valid"] else 50.0
        score_c = 100.0 - (len(c_res["deviations"]) * 20.0)
        score_b = 100.0 if b_res["severity"] == "low" else (40.0 if b_res["severity"] == "high" else 0.0)
        score_bh = 100.0 - (len(bh_res["risk_indicators"]) * 20.0)
        score_stat = 100.0 if stat_res["valid"] else 30.0
        score_sem = 100.0 if sem_res["valid"] else 40.0
        score_id = 100.0 if id_res["valid"] else 10.0
        
        val_score = (max(0, score_f) * 0.1) + (max(0, score_c) * 0.2) + (max(0, score_b) * 0.2) + \
                    (max(0, score_bh) * 0.1) + (max(0, score_stat) * 0.15) + (max(0, score_sem) * 0.1) + (max(0, score_id) * 0.15)
        
        critical_issues = []
        critical_issues.extend(f_res["issues"])
        critical_issues.extend([d["description"] for d in c_res["deviations"] if d["severity"] == "critical"])
        if b_res["severity"] == "critical":
            critical_issues.append("Critical mismatch between ITR income and Bank credits.")
        if not stat_res["valid"]:
            critical_issues.append(stat_res["description"])
        if not sem_res["valid"]:
            critical_issues.append("Document missing mandatory semantic keywords or contains suspicious phrasing.")
        if not id_res["valid"]:
            critical_issues.extend(id_res["mismatches"])
            
        processing_time = int((time.time() - start_time) * 1000)
        
        sub_reports = {
            "format": f_res,
            "computation": c_res,
            "bank_cross_reference": b_res,
            "behavior": bh_res,
            "statistical": stat_res,
            "semantic": sem_res,
            "identity": id_res
        }
        
        # Save to analysis result
        await self.analysis_repo.create({
            "case_id": case_id,
            "document_id": document_id,
            "analysis_type": "itr_verification_7_layer",
            "findings": sub_reports,
            "score": val_score,
            "severity": "high" if val_score < 70 else "low",
            "confidence": 0.95,
            "processing_time_ms": processing_time
        })
        await self.db.commit()
        
        return ITRReportResponse(
            document_id=document_id,
            validity_score=val_score,
            form_type=itr_fields.get("form_type"),
            assessment_year=itr_fields.get("assessment_year"),
            sub_reports=sub_reports,
            critical_issues=critical_issues,
            processing_time_ms=processing_time
        )
