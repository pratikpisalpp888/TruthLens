"""
TruthLens — Error Level Analysis (ELA).
"""

import cv2
import numpy as np
from typing import Dict, Any

class ErrorLevelAnalysis:
    def analyze(self, image: np.ndarray, quality: int = 90) -> Dict[str, Any]:
        """Performs ELA to detect image tampering."""
        # Save image as JPEG at given quality
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        result, encimg = cv2.imencode('.jpg', image, encode_param)
        
        if not result:
            raise ValueError("Failed to compress image for ELA")
            
        # Reload compressed image
        compressed = cv2.imdecode(encimg, 1)
        
        # Calculate absolute difference: original - compressed
        diff = cv2.absdiff(image, compressed)
        
        # Scale difference for visibility (multiply by 15)
        scale = 15
        diff_scaled = cv2.convertScaleAbs(diff, alpha=scale)
        
        # Convert to heatmap
        gray_diff = cv2.cvtColor(diff_scaled, cv2.COLOR_BGR2GRAY)
        heatmap = cv2.applyColorMap(gray_diff, cv2.COLORMAP_JET)
        
        # Detect high-intensity regions (threshold > 50)
        _, thresh = cv2.threshold(gray_diff, 50, 255, cv2.THRESH_BINARY)
        
        # Find contours of suspicious areas
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        suspicious_regions = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 100:  # ignore very small noise
                x, y, w, h = cv2.boundingRect(cnt)
                roi = gray_diff[y:y+h, x:x+w]
                intensity = float(np.mean(roi) / 255.0)
                suspicious_regions.append({
                    "bbox": [x, y, w, h],
                    "intensity": round(intensity, 2),
                    "area": float(area)
                })
        
        max_intensity = float(np.max(gray_diff) / 255.0)
        
        # Simple probability based on intensity and number of regions
        tampering_prob = min(1.0, (len(suspicious_regions) * 0.1) + (max_intensity * 0.5))
        
        # Create annotated image
        annotated = image.copy()
        for reg in suspicious_regions:
            x, y, w, h = reg["bbox"]
            cv2.rectangle(annotated, (x, y), (x+w, y+h), (0, 0, 255), 2)
            
        return {
            "heatmap": heatmap,
            "suspicious_regions": suspicious_regions,
            "max_intensity": max_intensity,
            "tampering_probability": tampering_prob,
            "analysis_image": annotated
        }
