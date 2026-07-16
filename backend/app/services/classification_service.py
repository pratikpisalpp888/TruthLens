"""
TruthLens — Rule-based Document Classifier.
"""

from typing import Tuple
import re

class DocumentClassifier:
    
    @staticmethod
    def classify(text: str, filename: str = "") -> Tuple[str, float]:
        """Classify document based on keyword heuristics and weights."""
        text = text.lower()
        
        scores = {
            "itr": 0.0,
            "sale_deed": 0.0,
            "bank_statement": 0.0,
            "land_record": 0.0,
            "balance_sheet": 0.0,
            "pan_card": 0.0
        }
        
        max_scores = {
            "itr": 49.0,
            "sale_deed": 46.0,
            "bank_statement": 39.0,
            "land_record": 49.0,
            "balance_sheet": 39.0,
            "pan_card": 28.0
        }
        
        # ITR indicators
        if "income tax return" in text: scores["itr"] += 10
        if "assessment year" in text: scores["itr"] += 8
        if "acknowledgement number" in text: scores["itr"] += 8
        if "form itr" in text: scores["itr"] += 10
        if "gross total income" in text: scores["itr"] += 7
        if "section 80" in text: scores["itr"] += 6
        if re.search(r'[a-z]{5}\d{4}[a-z]', text): scores["itr"] += 5
        
        # Sale Deed indicators
        if "sale deed" in text: scores["sale_deed"] += 10
        if "vendor" in text or "vendee" in text: scores["sale_deed"] += 8
        if "immovable property" in text: scores["sale_deed"] += 7
        if "registration" in text: scores["sale_deed"] += 6
        if "stamp duty" in text: scores["sale_deed"] += 7
        if "sub-registrar" in text: scores["sale_deed"] += 8
        
        # Bank Statement indicators
        if "statement of account" in text: scores["bank_statement"] += 10
        if "opening balance" in text: scores["bank_statement"] += 8
        if "closing balance" in text: scores["bank_statement"] += 8
        if "debit" in text or "credit" in text: scores["bank_statement"] += 7
        if re.search(r'[A-Z]{4}0[A-Z0-9]{6}', text.upper()): scores["bank_statement"] += 6 # IFSC
        if re.search(r'\b\d{9,18}\b', text): scores["bank_statement"] += 5 # Acct number
        
        # Land Record indicators
        if "survey number" in text: scores["land_record"] += 10
        if "7/12 extract" in text or "7/12" in text: scores["land_record"] += 10
        if "revenue record" in text: scores["land_record"] += 8
        if "khata" in text: scores["land_record"] += 8
        if "mutation" in text: scores["land_record"] += 7
        if "taluka" in text or "tehsil" in text: scores["land_record"] += 6
        
        # Balance Sheet indicators
        if "balance sheet" in text: scores["balance_sheet"] += 10
        if "assets" in text and "liabilities" in text: scores["balance_sheet"] += 8
        if "profit and loss" in text: scores["balance_sheet"] += 8
        if "shareholders equity" in text: scores["balance_sheet"] += 7
        if "auditor" in text: scores["balance_sheet"] += 6
        
        # PAN Card indicators
        if "permanent account number" in text: scores["pan_card"] += 10
        if "income tax department" in text: scores["pan_card"] += 8
        if re.search(r'[a-z]{5}\d{4}[a-z]', text): scores["pan_card"] += 10
        
        best_match = "other"
        best_confidence = 0.0
        
        for doc_type, score in scores.items():
            confidence = score / max_scores[doc_type]
            if confidence > best_confidence:
                best_confidence = confidence
                best_match = doc_type
                
        if best_confidence < 0.4:
            return "other", best_confidence
            
        return best_match, best_confidence
