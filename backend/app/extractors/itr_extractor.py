"""
TruthLens — ITR Extractor.
"""

import re
from typing import Dict, Any
from app.extractors.base_extractor import BaseExtractor

class ITRExtractor(BaseExtractor):
    async def extract(self, document_id: str, ocr_text: str, entities: dict) -> Dict[str, Any]:
        result = {}
        
        # From entities
        pan_numbers = entities.get("pan_numbers", [])
        if pan_numbers:
            result["pan"] = pan_numbers[0]
            
        ack_numbers = entities.get("itr_ack_numbers", [])
        if ack_numbers:
            result["acknowledgement_number"] = ack_numbers[0]
            
        assessment_years = entities.get("assessment_years", [])
        if assessment_years:
            result["assessment_year"] = assessment_years[0]
            
        # Regex based extraction
        form_match = re.search(r'ITR[- ]?[1-7]', ocr_text, re.IGNORECASE)
        if form_match:
            result["form_type"] = form_match.group(0).upper().replace(" ", "-")
            
        # Robust Fuzzy Extraction Fallbacks
        
        if not result.get("name_of_assessee"):
            name = self.extract_fuzzy_value(ocr_text, ["name of assessee", "name", "first name"], "text")
            if name: result["name_of_assessee"] = name
            
        if not result.get("gross_total_income"):
            gti = self.extract_fuzzy_value(ocr_text, ["gross total income", "gti", "total income"], "currency")
            if gti: result["gross_total_income"] = gti
            
        if not result.get("deductions_80c"):
            c80 = self.extract_fuzzy_value(ocr_text, ["80c", "deductions under 80c", "vi-a"], "currency")
            if c80: result["deductions_80c"] = c80
            
        if not result.get("tax_payable"):
            tax = self.extract_fuzzy_value(ocr_text, ["tax payable", "total tax", "tax computed"], "currency")
            if tax: result["tax_payable"] = tax
            
        if not result.get("refund_amount"):
            refund = self.extract_fuzzy_value(ocr_text, ["refund", "amount refundable"], "currency")
            if refund: result["refund_amount"] = refund
            
        return result
