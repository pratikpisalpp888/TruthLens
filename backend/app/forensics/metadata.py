"""
TruthLens — Metadata Analysis.
"""

import io
from typing import Dict, Any
from PyPDF2 import PdfReader
from PIL import Image
from PIL.ExifTags import TAGS

class MetadataAnalyzer:
    def analyze_pdf(self, pdf_bytes: bytes) -> Dict[str, Any]:
        """Extract and analyze PDF metadata."""
        anomalies = []
        result = {
            "creation_date": None,
            "modification_date": None,
            "creator_software": None,
            "anomalies": anomalies
        }
        
        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
            meta = reader.metadata
            if not meta:
                anomalies.append({
                    "type": "missing_metadata",
                    "severity": "medium",
                    "detail": "PDF contains no metadata",
                    "confidence": 1.0
                })
                return result
                
            c_date = meta.get("/CreationDate")
            m_date = meta.get("/ModDate")
            producer = meta.get("/Producer", "")
            creator = meta.get("/Creator", "")
            
            result["creation_date"] = str(c_date) if c_date else None
            result["modification_date"] = str(m_date) if m_date else None
            result["creator_software"] = str(producer) or str(creator)
            
            software_str = (str(producer) + " " + str(creator)).lower()
            suspicious_software = ["photoshop", "gimp", "canva", "illustrator", "coreldraw"]
            
            for sw in suspicious_software:
                if sw in software_str:
                    anomalies.append({
                        "type": "suspicious_software",
                        "severity": "high",
                        "detail": f"Created with image editing software: {sw}",
                        "confidence": 0.95
                    })
                    
            if c_date and m_date and c_date > m_date:
                anomalies.append({
                    "type": "date_inconsistency",
                    "severity": "high",
                    "detail": "Creation date is after modification date (time travel anomaly)",
                    "confidence": 0.95
                })
                
        except Exception as e:
            anomalies.append({
                "type": "parsing_error",
                "severity": "medium",
                "detail": f"Failed to parse PDF metadata: {str(e)}",
                "confidence": 1.0
            })
            
        return result

    def analyze_image(self, image_bytes: bytes) -> Dict[str, Any]:
        """Extract and analyze Image EXIF metadata."""
        anomalies = []
        result = {
            "creation_date": None,
            "modification_date": None,
            "creator_software": None,
            "anomalies": anomalies
        }
        
        try:
            img = Image.open(io.BytesIO(image_bytes))
            exif_data = img.getexif()
            
            if not exif_data:
                return result
                
            exif = {}
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                exif[str(tag)] = value
                
            software = exif.get("Software", "")
            result["creator_software"] = str(software)
            result["creation_date"] = str(exif.get("DateTimeOriginal", ""))
            result["modification_date"] = str(exif.get("DateTime", ""))
            
            software_str = str(software).lower()
            suspicious_software = ["photoshop", "gimp", "canva"]
            
            for sw in suspicious_software:
                if sw in software_str:
                    anomalies.append({
                        "type": "suspicious_software",
                        "severity": "high",
                        "detail": f"Created with image editing software: {sw}",
                        "confidence": 0.95
                    })
                    
            if exif.get("GPSInfo"):
                anomalies.append({
                    "type": "gps_data_present",
                    "severity": "low",
                    "detail": "Image contains GPS location data (unusual for scanned documents)",
                    "confidence": 0.8
                })
                
        except Exception:
            pass
            
        return result
