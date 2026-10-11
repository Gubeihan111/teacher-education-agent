"""Async repositories for aggregate persistence."""
from typing import Generic, TypeVar
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
T=TypeVar("T")
class SqlAlchemyRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: type[T]): self.session,self.model=session,model
    async def get(self, entity_id): return await self.session.get(self.model,entity_id)
    async def add(self, entity: T) -> T: self.session.add(entity); await self.session.flush(); return entity
    async def list_by(self, **filters) -> list[T]:
        result=await self.session.scalars(select(self.model).filter_by(**filters)); return list(result)
    async def save(self, entity: T) -> T: self.session.add(entity); await self.session.flush(); return entity
