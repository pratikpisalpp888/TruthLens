"""
TruthLens — Case Model.
"""

from sqlalchemy import Column, String, Float, Enum, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from app.db.base import Base, UUIDMixin, TimestampMixin

class Case(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "cases"

    case_number = Column(String(50), unique=True, index=True, nullable=False)
    applicant_name = Column(String(255), nullable=False)
    loan_type = Column(String(100), nullable=False)
    loan_amount = Column(Numeric(precision=18, scale=2), nullable=False)
    
    status = Column(
        Enum("created", "documents_uploaded", "analyzing", "analyzed", "decided", name="case_status_enum"),
        nullable=False,
        default="created"
    )
    risk_score = Column(Float, nullable=True)
    risk_category = Column(
        Enum("low", "medium", "high", name="risk_category_enum"),
        nullable=True
    )
    decision = Column(
        Enum("approved", "flagged", "rejected", "pending", name="decision_enum"),
        nullable=True
    )
    decision_reason = Column(String, nullable=True)
    
    officer_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    analysis_started_at = Column(DateTime(timezone=True), nullable=True)
    analysis_completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    officer = relationship("User", back_populates="cases")
    documents = relationship("Document", back_populates="case", cascade="all, delete-orphan")
    analysis_results = relationship("AnalysisResult", back_populates="case", cascade="all, delete-orphan")
