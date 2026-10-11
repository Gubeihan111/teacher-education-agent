"""bootstrap / lifespan.py placeholder."""

# TODO: implement during the API integration phase.
"""Own long-lived infrastructure resources."""
from contextlib import asynccontextmanager
from teacher_education_agent.infrastructure.checkpointer import postgres_checkpointer
@asynccontextmanager
async def lifespan(app):
    container=app.state.container
    async with postgres_checkpointer(container.settings.langgraph_checkpoint_url) as saver:
        container.checkpointer=saver
        yield
        container.checkpointer=None
