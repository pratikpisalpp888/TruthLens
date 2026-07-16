"""
TruthLens — Sale Deed Extractor.
"""

import re
from typing import Dict, Any
from app.extractors.base_extractor import BaseExtractor

class SaleDeedExtractor(BaseExtractor):
    async def extract(self, document_id: str, ocr_text: str, entities: dict) -> Dict[str, Any]:
        result = {}
        
        survey_numbers = entities.get("survey_numbers", [])
        if survey_numbers:
            result["survey_number"] = survey_numbers[0]
            
        dates = entities.get("dates", [])
        if dates:
            result["registration_date"] = dates[0]
            
        vendor_match = re.search(r'(?:Vendor|Seller)\s*[:\-]?\s*([A-Za-z\s]+)', ocr_text, re.IGNORECASE)
        if vendor_match:
            result["vendor_name"] = vendor_match.group(1).strip()
            
        vendee_match = re.search(r'(?:Vendee|Purchaser|Buyer)\s*[:\-]?\s*([A-Za-z\s]+)', ocr_text, re.IGNORECASE)
        if vendee_match:
            result["vendee_name"] = vendee_match.group(1).strip()
            
        area_match = re.search(r'(?:Area|Extent)\s*[:\-]?\s*([\d\.]+\s*(?:acres|sqft|sqm|sq ft|sq meters|hectares))', ocr_text, re.IGNORECASE)
        if area_match:
            result["area"] = area_match.group(1).strip()
            
        value_match = re.search(r'(?:Sale Value|Consideration|Sale Price)\s*[:\-]?\s*(?:Rs\.?|₹|INR)?\s*([\d,]+\.?\d*)', ocr_text, re.IGNORECASE)
        if value_match:
            result["sale_value"] = value_match.group(1).strip()
            
        stamp_match = re.search(r'(?:Stamp Duty)\s*[:\-]?\s*(?:Rs\.?|₹|INR)?\s*([\d,]+\.?\d*)', ocr_text, re.IGNORECASE)
        if stamp_match:
            result["stamp_duty"] = stamp_match.group(1).strip()
            
        sub_match = re.search(r'(?:Sub-Registrar|Sub Registrar Office)\s*[:\-]?\s*([A-Za-z\s]+)', ocr_text, re.IGNORECASE)
        if sub_match:
            result["sub_registrar_office"] = sub_match.group(1).strip()
            
        # ── Fuzzy NLP Fallbacks (handles messy OCR) ──
        if not result.get("vendor_name"):
            vendor = self.extract_fuzzy_value(ocr_text, ["vendor", "seller"], "text")
            if vendor: result["vendor_name"] = vendor
            
        if not result.get("vendee_name"):
            vendee = self.extract_fuzzy_value(ocr_text, ["vendee", "purchaser", "buyer"], "text")
            if vendee: result["vendee_name"] = vendee
            
        if not result.get("sale_value"):
            sale = self.extract_fuzzy_value(ocr_text, ["sale value", "consideration", "sale price"], "currency")
            if sale: result["sale_value"] = sale
            
        if not result.get("stamp_duty"):
            stamp = self.extract_fuzzy_value(ocr_text, ["stamp duty", "duty paid"], "currency")
            if stamp: result["stamp_duty"] = stamp
            
        if not result.get("sub_registrar_office"):
            office = self.extract_fuzzy_value(ocr_text, ["sub-registrar", "sub registrar office", "sro"], "text")
            if office: result["sub_registrar_office"] = office
            
        return result
