"""
TruthLens — Land Record Extractor.
"""

import re
from typing import Dict, Any
from app.extractors.base_extractor import BaseExtractor

class LandRecordExtractor(BaseExtractor):
    async def extract(self, document_id: str, ocr_text: str, entities: dict) -> Dict[str, Any]:
        result = {}
        
        survey_numbers = entities.get("survey_numbers", [])
        if survey_numbers:
            result["survey_number"] = survey_numbers[0]
            
        owner_match = re.search(r'(?:Owner Name|Khatedar Name|Name of Occupant)\s*[:\-]?\s*([A-Za-z\s]+)', ocr_text, re.IGNORECASE)
        if owner_match:
            result["owner_name"] = owner_match.group(1).strip()
            
        area_match = re.search(r'(?:Total Area|Area)\s*[:\-]?\s*([\d\.]+\s*(?:acres|hectares|sqm|guntas|ares))', ocr_text, re.IGNORECASE)
        if area_match:
            result["area"] = area_match.group(1).strip()
            
        village_match = re.search(r'(?:Village|Gram)\s*[:\-]?\s*([A-Za-z\s]+)', ocr_text, re.IGNORECASE)
        if village_match:
            result["village"] = village_match.group(1).strip()
            
        taluka_match = re.search(r'(?:Taluka|Tehsil)\s*[:\-]?\s*([A-Za-z\s]+)', ocr_text, re.IGNORECASE)
        if taluka_match:
            result["taluka"] = taluka_match.group(1).strip()
            
        district_match = re.search(r'(?:District|Zilla)\s*[:\-]?\s*([A-Za-z\s]+)', ocr_text, re.IGNORECASE)
        if district_match:
            result["district"] = district_match.group(1).strip()
            
        return result
