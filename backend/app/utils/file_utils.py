"""
TruthLens — File Processing Utilities.
"""

import io
from typing import List
from fastapi import UploadFile
import magic
from PIL import Image
from pdf2image import convert_from_bytes
import PyPDF2

from app.core.config import settings

def pdf_to_images(pdf_bytes: bytes) -> List[Image.Image]:
    """Convert PDF pages to PIL Images."""
    try:
        images = convert_from_bytes(pdf_bytes)
        return images
    except Exception:
        return []

def get_mime_type(file_bytes: bytes) -> str:
    """Detect MIME type using python-magic."""
    return magic.from_buffer(file_bytes, mime=True)

def validate_file(file: UploadFile, file_bytes: bytes) -> bool:
    """Validate file type and size."""
    if len(file_bytes) > settings.MAX_UPLOAD_SIZE_BYTES:
        return False
        
    mime_type = get_mime_type(file_bytes)
    allowed_mimes = ["application/pdf", "image/jpeg", "image/png", "image/tiff"]
    if mime_type not in allowed_mimes:
        return False
        
    return True

def get_page_count(file_bytes: bytes, mime_type: str) -> int:
    """Count PDF pages. Returns 1 for images."""
    if mime_type == "application/pdf":
        try:
            reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            return len(reader.pages)
        except Exception:
            return 1
    return 1
