"""
TruthLens — Analysis Result Model.
"""

from sqlalchemy import Column, String, Integer, Float, Enum, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base, UUIDMixin, TimestampMixin

class AnalysisResult(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "analysis_results"

    case_id = Column(String(36), ForeignKey("cases.id", ondelete="CASCADE"), index=True, nullable=False)
    document_id = Column(String(36), ForeignKey("documents.id", ondelete="CASCADE"), nullable=True)
    
    analysis_type = Column(
        Enum("forensics", "cross_document", "itr_validation", "fraud_dna", "compliance", "agent_decision", name="analysis_type_enum"),
        nullable=False
    )
    agent_name = Column(String(100), nullable=True)
    
    findings = Column(JSON, nullable=False)
    score = Column(Float, nullable=True)
    
    severity = Column(
        Enum("low", "medium", "high", "critical", name="severity_enum"),
        nullable=True
    )
    confidence = Column(Float, nullable=True)
    
    evidence_paths = Column(JSON, nullable=True)
    processing_time_ms = Column(Integer, nullable=False)

    # Relationships
    case = relationship("Case", back_populates="analysis_results")
    document = relationship("Document", back_populates="analysis_results")
