"""PostgreSQL-backed LangGraph checkpoint lifecycle."""
from contextlib import asynccontextmanager
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

@asynccontextmanager
async def postgres_checkpointer(connection_string: str):
    async with AsyncPostgresSaver.from_conn_string(connection_string) as saver:
        await saver.setup()
        yield saver
