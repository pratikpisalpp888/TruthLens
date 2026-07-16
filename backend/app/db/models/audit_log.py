"""
TruthLens — Audit Log Model.
"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base, UUIDMixin

class AuditLog(UUIDMixin, Base):
    __tablename__ = "audit_logs"

    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    action = Column(String(100), index=True, nullable=False)
    
    resource_type = Column(String(100), nullable=False)
    resource_id = Column(String(36), nullable=True)
    
    details = Column(JSONB, nullable=True)
    ip_address = Column(String(45), nullable=True)
    
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow, index=True, nullable=False)

    # Relationships
    user = relationship("User", back_populates="audit_logs")
