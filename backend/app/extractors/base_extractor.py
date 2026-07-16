"""
TruthLens — Base Extractor.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseExtractor(ABC):
    @abstractmethod
    async def extract(self, document_id: str, ocr_text: str, entities: dict) -> Dict[str, Any]:
        """Extract structured fields from OCR text and entities."""
        pass

    def extract_fuzzy_value(self, ocr_text: str, anchors: list[str], value_type: str = "currency") -> str | None:
        """
        Fuzzy NLP Key-Value Extraction.
        Finds the closest match to any anchor in the text, then extracts the adjacent value.
        """
        try:
            from thefuzz import process, fuzz
            import re
            
            # Split text into lines or chunks
            lines = [line.strip() for line in ocr_text.split('\n') if line.strip()]
            if not lines:
                return None
                
            # Find the line that best matches our anchor terms
            best_match_line = None
            highest_score = 0
            
            for line in lines:
                # Compare line against all anchors
                match, score = process.extractOne(line.lower(), anchors, scorer=fuzz.partial_ratio)
                if score > highest_score:
                    highest_score = score
                    best_match_line = line
                    
            if highest_score < 75 or not best_match_line:
                return None
                
            # We found a matching line! Now extract the value from this line, 
            # or if it's just the label, the next line.
            text_to_search = best_match_line
            # Also append the next line just in case the value wrapped
            try:
                idx = lines.index(best_match_line)
                if idx + 1 < len(lines):
                    text_to_search += " " + lines[idx+1]
            except ValueError:
                pass
                
            if value_type == "currency":
                # Find amount: Rs. 1,23,456.00 or 123456
                matches = re.findall(r'(?:Rs\.?|₹|INR)?\s*([\d,]+\.?\d*)', text_to_search, re.IGNORECASE)
                # Filter out pure dates or small numbers if multiple found, usually we want the largest or the first big one
                valid_amounts = []
                for m in matches:
                    clean_val = m.replace(',', '')
                    if clean_val and float(clean_val) > 0:
                        valid_amounts.append(m)
                
                if valid_amounts:
                    # Return the first substantial amount found near the anchor
                    return valid_amounts[-1] if len(valid_amounts) > 1 else valid_amounts[0]
                    
            elif value_type == "pan":
                match = re.search(r'[A-Z]{5}[0-9]{4}[A-Z]', text_to_search.upper())
                if match:
                    return match.group(0)
                    
            elif value_type == "date":
                match = re.search(r'\b\d{1,2}[/\-.]\d{1,2}[/\-.]\d{2,4}\b', text_to_search)
                if match:
                    return match.group(0)
                    
            elif value_type == "text":
                # E.g. "Name of Assessee: John Doe"
                # Strip out the anchor part and return the rest
                cleaned = best_match_line
                for anchor in anchors:
                    # case insensitive replace
                    pattern = re.compile(re.escape(anchor), re.IGNORECASE)
                    cleaned = pattern.sub('', cleaned)
                # clean up colons and spaces
                cleaned = re.sub(r'^[\s:\-]+', '', cleaned).strip()
                if cleaned:
                    return cleaned
                
            return None
            
        except Exception as e:
            return None
