"""
TruthLens — Audit Service.
"""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.audit_log import AuditLog

class AuditService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log(self, user_id: str, action: str, resource_type: str, resource_id: Optional[str] = None, details: dict = None, ip_address: Optional[str] = None):
        """Creates an audit log entry."""
        audit_entry = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address
        )
        self.db.add(audit_entry)
        await self.db.flush()
