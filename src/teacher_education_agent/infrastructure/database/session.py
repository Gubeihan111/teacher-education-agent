"""Async PostgreSQL session factory."""
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from teacher_education_agent.core.config import Settings
def build_engine(settings: Settings):
    return create_async_engine(settings.database_url, pool_pre_ping=True)
def build_session_factory(settings: Settings) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(build_engine(settings), expire_on_commit=False)
