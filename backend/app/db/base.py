"""
TruthLens — SQLAlchemy Base and Mixins.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, String, MetaData
from sqlalchemy.orm import declarative_base, declared_attr
from sqlalchemy.sql import func
from uuid_utils import uuid7

# Naming convention for constraints
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

class CustomBase:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"

Base = declarative_base(cls=CustomBase, metadata=metadata)

class UUIDMixin:
    """Provides a UUID7 primary key."""
    id = Column(String(36), primary_key=True, default=lambda: str(uuid7()), index=True)

class TimestampMixin:
    """Provides created_at and updated_at timestamps."""
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
