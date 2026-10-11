"""Transaction unit-of-work protocol placeholder."""

from typing import Protocol
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class UnitOfWork(Protocol):
    """Transaction boundary controlled by application code, never an LLM."""

    ...

class SqlAlchemyUnitOfWork:
    def __init__(self, factory: async_sessionmaker[AsyncSession]):
        self.factory, self.session = factory, None
    async def __aenter__(self):
        self.session = self.factory()
        return self
    async def __aexit__(self, exc_type, exc, tb):
        if self.session is None: return
        if exc_type is None: await self.session.commit()
        else: await self.session.rollback()
        await self.session.close()
