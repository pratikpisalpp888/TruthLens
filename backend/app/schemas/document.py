"""
TruthLens — Document Schemas.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel

class DocumentResponse(BaseModel):
    id: str
    case_id: str
    original_filename: str
    file_size: int
    mime_type: str
    document_type: Optional[str] = None
    processing_status: str
    created_at: datetime
    extracted_entities: Optional[Dict[str, Any]] = None
    extracted_fields: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    
    class Config:
        from_attributes = True
