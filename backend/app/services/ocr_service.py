"""
TruthLens — OCR Service.
"""

from typing import Dict, Any, List
import asyncio
import re
from uuid import UUID

try:
    from paddleocr import PaddleOCR
    # Forcing Paddle off for lightning-fast demo. PaddleOCR init blocks the thread for minutes.
    PADDLE_AVAILABLE = False
except Exception as e:
    print(f"DEBUG: PaddleOCR import failed: {e}")
    PADDLE_AVAILABLE = False
import numpy as np

from app.core.config import settings
from app.services.storage_service import StorageService
from app.utils.encryption import decrypt_file
from app.utils.file_utils import pdf_to_images, get_mime_type

class OCRService:
    def __init__(self):
        # Initialize PaddleOCR (CPU mode for compatibility)
        if PADDLE_AVAILABLE:
            self.ocr = PaddleOCR(
                use_angle_cls=True,
                lang='en',
                use_gpu=False,
                show_log=False
            )
        else:
            self.ocr = None
        self.storage = StorageService()

    def detect_language(self, text: str) -> str:
        """Simple script detection based on character ranges."""
        if re.search(r'[\u0900-\u097F]', text): return "hindi" # Devanagari
        if re.search(r'[\u0B80-\u0BFF]', text): return "tamil"
        if re.search(r'[\u0C00-\u0C7F]', text): return "telugu"
        if re.search(r'[\u0C80-\u0CFF]', text): return "kannada"
        
        # If no specific Indian scripts are found, assume English/Latin
        if re.search(r'[A-Za-z]', text): return "english"
        
        return "multilingual"

    async def extract_text_from_bytes(self, file_bytes: bytes, mime_type: str) -> Dict[str, Any]:
        """Extract text from raw bytes without storage or decryption."""
        full_text_list = []
        pages = []
        
        # FAST PATH FOR PDFs (Instant text extraction, bypasses slow OCR model)
        if mime_type == "application/pdf":
            try:
                import fitz
                doc = fitz.open(stream=file_bytes, filetype="pdf")
                for i, page in enumerate(doc):
                    text = page.get_text().strip()
                    full_text_list.append(text)
                    pages.append({
                        "page_number": i + 1,
                        "text": text,
                        "blocks": [{"text": text, "confidence": 1.0, "bounding_box": []}] if text else [],
                        "language": self.detect_language(text)
                    })
                doc.close()
                
                full_document_text = "\n\n".join(full_text_list)
                return {
                    "full_text": full_document_text,
                    "page_count": len(pages),
                    "pages": pages,
                    "overall_confidence": 1.0,
                    "primary_language": self.detect_language(full_document_text)
                }
            except Exception as e:
                import structlog
                structlog.get_logger().error(f"PyMuPDF failed, falling back to OCR: {e}")
                # Fall through to slow OCR path if PyMuPDF fails
                
        # SLOW OCR PATH FOR IMAGES (or fallback)
        images = []
        if mime_type == "application/pdf":
            loop = asyncio.get_event_loop()
            images = await loop.run_in_executor(None, pdf_to_images, file_bytes)
        else:
            from PIL import Image
            import io
            images = [Image.open(io.BytesIO(file_bytes))]
            
        for i, img in enumerate(images):
            img_np = np.array(img.convert('RGB'))
            
            blocks = []
            page_text = []
            
            if self.ocr is not None:
                try:
                    loop = asyncio.get_event_loop()
                    result = await loop.run_in_executor(None, self.ocr.ocr, img_np, True)
                    
                    if result and result[0]:
                        for line in result[0]:
                            box = line[0]
                            text = line[1][0]
                            conf = line[1][1]
                            
                            blocks.append({
                                "text": text,
                                "confidence": conf,
                                "bounding_box": box
                            })
                            page_text.append(text)
                except Exception as e:
                    logger.error(f"PaddleOCR processing failed for page {i+1}: {e}")
            else:
                try:
                    import pytesseract
                    loop = asyncio.get_event_loop()
                    text = await loop.run_in_executor(None, pytesseract.image_to_string, img)
                    if text.strip():
                        page_text.append(text.strip())
                        blocks.append({
                            "text": text.strip(),
                            "confidence": 0.8,
                            "bounding_box": []
                        })
                except Exception as e:
                    logger.error(f"Tesseract processing failed for page {i+1}: {e}")
            
            joined_page_text = "\n".join(page_text)
            full_text_list.append(joined_page_text)
            
            pages.append({
                "page_number": i + 1,
                "text": joined_page_text,
                "blocks": blocks,
                "language": self.detect_language(joined_page_text)
            })
            
        full_document_text = "\n\n".join(full_text_list)
        all_confs = [block["confidence"] for page in pages for block in page["blocks"]]
        overall_confidence = sum(all_confs) / len(all_confs) if all_confs else 0.0
        
        return {
            "full_text": full_document_text,
            "page_count": len(images),
            "pages": pages,
            "overall_confidence": overall_confidence,
            "primary_language": self.detect_language(full_document_text)
        }

    async def extract_text(self, document_id: str, file_path: str, mime_type: str) -> Dict[str, Any]:
        """Extract text from document via OCR, downloading and decrypting first."""
        encrypted_bytes = await self.storage.download(file_path)
        decrypted_bytes = decrypt_file(encrypted_bytes, settings.ENCRYPTION_KEY)
        res = await self.extract_text_from_bytes(decrypted_bytes, mime_type)
        res["document_id"] = document_id
        res["language"] = res["primary_language"]
        return res
