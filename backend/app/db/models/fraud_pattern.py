"""
TruthLens — Fraud Pattern Model.
"""

from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.dialects.postgresql import JSONB

from app.db.base import Base, UUIDMixin, TimestampMixin

class FraudPattern(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "fraud_patterns"

    pattern_name = Column(String(255), nullable=False)
    pattern_type = Column(String(100), nullable=False)
    document_type = Column(String(100), nullable=False)
    
    feature_vector_id = Column(String(36), nullable=False)
    features = Column(JSONB, nullable=False)
    
    description = Column(String, nullable=False)
    severity = Column(String(50), nullable=False)
    
    occurrences = Column(Integer, default=1, nullable=False)
    source_case_ids = Column(JSONB, nullable=False)
    is_confirmed = Column(Boolean, default=False, nullable=False)
