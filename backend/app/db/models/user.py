"""
TruthLens — User Model.
"""

from sqlalchemy import Column, String, Boolean, Enum, DateTime
from sqlalchemy.orm import relationship

from app.db.base import Base, UUIDMixin, TimestampMixin

class User(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "users"

    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(Enum("officer", "admin", name="user_role_enum"), nullable=False, default="officer")
    is_active = Column(Boolean, default=True, nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    cases = relationship("Case", back_populates="officer", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")
