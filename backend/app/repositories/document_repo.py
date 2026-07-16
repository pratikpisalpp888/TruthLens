"""
TruthLens — Document Repository.
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository
from app.db.models.document import Document

class DocumentRepository(BaseRepository[Document]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Document)

    async def get_by_case(self, case_id: str) -> List[Document]:
        query = select(self.model).where(self.model.case_id == case_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_status(self, status: str) -> List[Document]:
        query = select(self.model).where(self.model.processing_status == status)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def update_processing_status(self, id: str, status: str, error_message: Optional[str] = None) -> Optional[Document]:
        data = {"processing_status": status}
        if error_message is not None:
            data["error_message"] = error_message
        return await self.update(id, data)
