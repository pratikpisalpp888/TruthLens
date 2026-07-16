"""
TruthLens — Fraud Pattern Repository.
"""

from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository
from app.db.models.fraud_pattern import FraudPattern

class FraudPatternRepository(BaseRepository[FraudPattern]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, FraudPattern)

    async def get_by_type(self, pattern_type: str) -> List[FraudPattern]:
        query = select(self.model).where(self.model.pattern_type == pattern_type)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_confirmed(self) -> List[FraudPattern]:
        query = select(self.model).where(self.model.is_confirmed == True)
        result = await self.session.execute(query)
        return list(result.scalars().all())
