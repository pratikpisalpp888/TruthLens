"""
TruthLens — Font Consistency Analysis.
"""

import numpy as np
from typing import Dict, Any

class FontAnalyzer:
    def analyze(self, image: np.ndarray, ocr_blocks: list) -> Dict[str, Any]:
        """
        Analyzes OCR text blocks for font inconsistencies.
        (Simplified implementation for document forensics)
        """
        inconsistencies = []
        font_groups = []
        
        # In a full implementation, we would extract each bounding box,
        # calculate stroke width transform (SWT), height variance, etc.
        # Here we mock the structural logic based on block heights as an example.
        
        heights = []
        for block in ocr_blocks:
            bbox = block.get("bbox", [])
            if len(bbox) == 4:
                # Assuming format [[x1,y1], [x2,y1], [x2,y2], [x1,y2]] or [x,y,w,h]
                # If paddleOCR format: [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
                try:
                    h = bbox[2][1] - bbox[0][1]
                    heights.append(h)
                except Exception:
                    pass
                    
        anomaly_score = 0.0
        
        if len(heights) > 5:
            mean_h = np.mean(heights)
            std_h = np.std(heights)
            
            if std_h > (mean_h * 0.5):
                inconsistencies.append({
                    "type": "high_variance",
                    "detail": "Extremely high variance in text block heights detected."
                })
                anomaly_score = 0.4
                
        return {
            "font_groups": font_groups,
            "inconsistencies": inconsistencies,
            "anomaly_score": anomaly_score
        }
