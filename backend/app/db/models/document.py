"""
TruthLens — Document Model.
"""

from sqlalchemy import Column, String, Integer, Float, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base, UUIDMixin, TimestampMixin

class Document(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "documents"

    case_id = Column(String(36), ForeignKey("cases.id", ondelete="CASCADE"), index=True, nullable=False)
    original_filename = Column(String(255), nullable=False)
    stored_filename = Column(String(255), nullable=False)
    file_path = Column(String(1024), nullable=False)
    file_hash = Column(String(64), nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String(100), nullable=False)
    
    document_type = Column(
        Enum("itr", "sale_deed", "bank_statement", "land_record", "balance_sheet", "pan_card", "other", name="doc_type_enum"),
        nullable=True
    )
    classification_confidence = Column(Float, nullable=True)
    
    processing_status = Column(
        Enum("uploaded", "classified", "ocr_done", "extracted", "analyzed", "error", name="processing_status_enum"),
        nullable=False,
        default="uploaded"
    )
    
    ocr_text = Column(String, nullable=True)
    extracted_entities = Column(JSONB, nullable=True)
    extracted_fields = Column(JSONB, nullable=True)
    
    language_detected = Column(String(50), nullable=True)
    page_count = Column(Integer, nullable=True)
    error_message = Column(String, nullable=True)

    # Relationships
    case = relationship("Case", back_populates="documents")
    analysis_results = relationship("AnalysisResult", back_populates="document", cascade="all, delete-orphan")
