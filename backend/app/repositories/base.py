"""
TruthLens — Base Repository.
"""

from typing import Generic, TypeVar, Type, Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.sql import func

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self.session = session
        self.model = model

    async def get_by_id(self, id: str) -> Optional[ModelType]:
        result = await self.session.execute(select(self.model).filter(self.model.id == id))
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100, filters: Optional[Dict[str, Any]] = None) -> List[ModelType]:
        query = select(self.model)
        if filters:
            for k, v in filters.items():
                query = query.filter(getattr(self.model, k) == v)
        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create(self, data: Dict[str, Any]) -> ModelType:
        obj = self.model(**data)
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def update(self, id: str, data: Dict[str, Any]) -> Optional[ModelType]:
        query = update(self.model).where(self.model.id == id).values(**data).execution_options(synchronize_session="fetch")
        await self.session.execute(query)
        await self.session.flush()
        return await self.get_by_id(id)

    async def delete(self, id: str) -> bool:
        query = delete(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        await self.session.flush()
        return result.rowcount > 0

    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        query = select(func.count()).select_from(self.model)
        if filters:
            for k, v in filters.items():
                query = query.filter(getattr(self.model, k) == v)
        result = await self.session.execute(query)
        return result.scalar_one()

    async def exists(self, id: str) -> bool:
        result = await self.count({"id": id})
        return result > 0
