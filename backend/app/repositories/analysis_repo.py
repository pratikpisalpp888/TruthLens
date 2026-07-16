"""
TruthLens — Analysis Result Repository.
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository
from app.db.models.analysis import AnalysisResult

class AnalysisResultRepository(BaseRepository[AnalysisResult]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, AnalysisResult)

    async def get_by_case(self, case_id: str) -> List[AnalysisResult]:
        query = select(self.model).where(self.model.case_id == case_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_type(self, analysis_type: str) -> List[AnalysisResult]:
        query = select(self.model).where(self.model.analysis_type == analysis_type)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_latest(self, case_id: str, analysis_type: str) -> Optional[AnalysisResult]:
        query = (
            select(self.model)
            .where(self.model.case_id == case_id, self.model.analysis_type == analysis_type)
            .order_by(self.model.created_at.desc())
        )
        result = await self.session.execute(query)
        return result.scalars().first()
