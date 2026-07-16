"""
TruthLens — NER Service.
"""

import re
from typing import Dict, Any, List
try:
    import spacy as _spacy
    SPACY_AVAILABLE = True
except Exception:
    SPACY_AVAILABLE = False

class NERService:
    def __init__(self):
        self.nlp = None
        if SPACY_AVAILABLE:
            try:
                self.nlp = _spacy.load("en_core_web_sm")
            except OSError:
                try:
                    import spacy.cli
                    spacy.cli.download("en_core_web_sm")
                    self.nlp = _spacy.load("en_core_web_sm")
                except Exception:
                    pass  # Fall back to regex-only
            
        # We handle custom regex patterns inside extract_entities
        
    async def extract_entities(self, document_id: str, ocr_text: str) -> Dict[str, Any]:
        """Extract named entities and custom Indian patterns."""
        import asyncio
        loop = asyncio.get_event_loop()
        
        # Run spaCy NER in thread (if model available)
        spacy_ents = []
        if self.nlp is not None:
            doc = await loop.run_in_executor(None, self.nlp, ocr_text)
            spacy_ents = doc.ents
        
        entities = {
            "persons": [],
            "organizations": [],
            "locations": [],
            "dates": [],
            "amounts": [],
            "pan_numbers": [],
            "aadhaar_numbers": [],
            "account_numbers": [],
            "ifsc_codes": [],
            "survey_numbers": [],
            "itr_ack_numbers": [],
            "assessment_years": []
        }
        
        # Collect spaCy entities
        for ent in spacy_ents:
            if ent.label_ == "PERSON":
                entities["persons"].append(ent.text)
            elif ent.label_ == "ORG":
                entities["organizations"].append(ent.text)
            elif ent.label_ in ["GPE", "LOC"]:
                entities["locations"].append(ent.text)
                
        # Custom regex patterns
        pan_matches = re.findall(r'[A-Z]{5}[0-9]{4}[A-Z]{1}', ocr_text)
        entities["pan_numbers"].extend(pan_matches)
        
        aadhaar_matches = re.findall(r'\b\d{4}\s?\d{4}\s?\d{4}\b', ocr_text)
        entities["aadhaar_numbers"].extend(aadhaar_matches)
        
        ifsc_matches = re.findall(r'[A-Z]{4}0[A-Z0-9]{6}', ocr_text)
        entities["ifsc_codes"].extend(ifsc_matches)
        
        account_matches = re.findall(r'\b\d{9,18}\b', ocr_text)
        # Filter out aadhar from accounts roughly
        for acc in account_matches:
            if len(acc) != 12 or acc not in [a.replace(" ","") for a in aadhaar_matches]:
                entities["account_numbers"].append(acc)
                
        survey_matches = re.findall(r'(?:Survey|Sy|S\.?\s*No\.?)\s*[:.]?\s*\d+[\/\-]?\d*[A-Za-z]?', ocr_text, re.IGNORECASE)
        entities["survey_numbers"].extend(survey_matches)
        
        amount_matches = re.findall(r'(?:Rs\.?|₹|INR)\s*[\d,]+\.?\d*', ocr_text, re.IGNORECASE)
        entities["amounts"].extend(amount_matches)
        
        date_matches = re.findall(r'\b\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4}\b', ocr_text)
        entities["dates"].extend(date_matches)
        
        ack_matches = re.findall(r'\b\d{15}\b', ocr_text)
        entities["itr_ack_numbers"].extend(ack_matches)
        
        ay_matches = re.findall(r'(?:AY|Assessment Year)\s*:?\s*\d{4}\s*[-–]\s*\d{2,4}', ocr_text, re.IGNORECASE)
        entities["assessment_years"].extend(ay_matches)
        
        # Deduplicate all lists
        for key in entities:
            entities[key] = list(set(entities[key]))
            
        return {
            "document_id": document_id,
            "entities": entities
        }
