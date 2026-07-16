"""
TruthLens — Case Repository.
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository
from app.db.models.case import Case

class CaseRepository(BaseRepository[Case]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Case)

    async def get_by_status(self, status: str) -> List[Case]:
        query = select(self.model).where(self.model.status == status)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_officer(self, officer_id: str) -> List[Case]:
        query = select(self.model).where(self.model.officer_id == officer_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_with_documents(self, id: str) -> Optional[Case]:
        query = select(self.model).options(selectinload(self.model.documents)).where(self.model.id == id)
        result = await self.session.execute(query)
        return result.scalars().first()
