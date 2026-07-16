"""
TruthLens — Audit Log Repository.
"""

from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository
from app.db.models.audit_log import AuditLog

class AuditLogRepository(BaseRepository[AuditLog]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, AuditLog)

    async def get_by_user(self, user_id: str) -> List[AuditLog]:
        query = select(self.model).where(self.model.user_id == user_id).order_by(self.model.timestamp.desc())
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_resource(self, resource_type: str, resource_id: str) -> List[AuditLog]:
        query = select(self.model).where(
            self.model.resource_type == resource_type,
            self.model.resource_id == resource_id
        ).order_by(self.model.timestamp.desc())
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_recent(self, limit: int = 100) -> List[AuditLog]:
        query = select(self.model).order_by(self.model.timestamp.desc()).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def log(self, user_id: str, action: str, resource_type: str = "", resource_id: str = "", details: dict = None, ip_address: str = None) -> AuditLog:
        from datetime import datetime
        entry = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details or {},
            ip_address=ip_address,
            timestamp=datetime.utcnow(),
        )
        self.session.add(entry)
        return entry
