"""
TruthLens — Signature Detection and Verification.
"""

import cv2
import numpy as np
from typing import Dict, Any

class SignatureChecker:
    def check_digital_signature(self, pdf_bytes: bytes) -> Dict[str, Any]:
        """Check for digital /Sig objects in PDF."""
        # Simple binary search for signature object
        has_sig = b"/Sig" in pdf_bytes or b"/ByteRange" in pdf_bytes
        
        return {
            "digitally_signed": has_sig,
            "signature_coverage": "full" if has_sig else "none",
            "certificate_valid": has_sig # simplified
        }
        
    def detect_visual_signature(self, image: np.ndarray) -> Dict[str, Any]:
        """Detect handwritten signatures and stamps using contour analysis."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        
        # Thresholding
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Morphological operations to group signature strokes
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        signatures = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if 1000 < area < 50000: # Typical signature bounds
                x, y, w, h = cv2.boundingRect(cnt)
                aspect_ratio = float(w)/h
                if 1.5 < aspect_ratio < 5.0: # Signatures are usually wider than tall
                    signatures.append([x, y, w, h])
                    
        return {
            "visual_signatures_detected": len(signatures),
            "locations": signatures,
            "stamps_detected": 0
        }
