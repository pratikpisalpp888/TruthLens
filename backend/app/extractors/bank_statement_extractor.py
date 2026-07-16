"""
TruthLens — Bank Statement Extractor.
"""

import re
from typing import Dict, Any
from app.extractors.base_extractor import BaseExtractor

class BankStatementExtractor(BaseExtractor):
    async def extract(self, document_id: str, ocr_text: str, entities: dict) -> Dict[str, Any]:
        result = {}
        
        account_numbers = entities.get("account_numbers", [])
        if account_numbers:
            result["account_number"] = account_numbers[0]
            
        ifsc_codes = entities.get("ifsc_codes", [])
        if ifsc_codes:
            result["ifsc_code"] = ifsc_codes[0]
            
        # Fast regex first pass (keeps speed for well-formatted docs)
        name_match = re.search(r'(?:Name|Account Holder)\s*[:\-]?\s*([A-Za-z\s]+)', ocr_text, re.IGNORECASE)
        if name_match:
            result["account_holder_name"] = name_match.group(1).strip()
            
        bank_match = re.search(r'(?:Bank Name|Bank)\s*[:\-]?\s*([A-Za-z\s]+)', ocr_text, re.IGNORECASE)
        if bank_match:
            result["bank_name"] = bank_match.group(1).strip()
            
        open_match = re.search(r'(?:Opening Balance)\s*[:\-]?\s*(?:Rs\.?|₹|INR)?\s*([\d,]+\.?\d*)', ocr_text, re.IGNORECASE)
        if open_match:
            result["opening_balance"] = open_match.group(1).strip()
            
        close_match = re.search(r'(?:Closing Balance|Available Balance)\s*[:\-]?\s*(?:Rs\.?|₹|INR)?\s*([\d,]+\.?\d*)', ocr_text, re.IGNORECASE)
        if close_match:
            result["closing_balance"] = close_match.group(1).strip()
        
        # Count transactions roughly by looking for date patterns at line starts
        transactions = re.findall(r'^\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}', ocr_text, re.MULTILINE)
        result["number_of_transactions"] = len(transactions)
        
        # ── Fuzzy NLP Fallbacks (handles messy OCR / unconventional layouts) ──
        if not result.get("account_holder_name"):
            name = self.extract_fuzzy_value(ocr_text, ["account holder", "name", "customer name"], "text")
            if name: result["account_holder_name"] = name
            
        if not result.get("opening_balance"):
            opening = self.extract_fuzzy_value(ocr_text, ["opening balance", "balance brought forward", "b/f", "opening"], "currency")
            if opening: result["opening_balance"] = opening
            
        if not result.get("closing_balance"):
            closing = self.extract_fuzzy_value(ocr_text, ["closing balance", "available balance", "balance carried forward", "c/f"], "currency")
            if closing: result["closing_balance"] = closing
            
        if not result.get("bank_name"):
            bank = self.extract_fuzzy_value(ocr_text, ["bank name", "branch", "bank"], "text")
            if bank: result["bank_name"] = bank
            
        return result
