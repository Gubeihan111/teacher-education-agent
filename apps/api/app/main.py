"""Teacher education API."""
from fastapi import FastAPI
from .api.v1.router import router
from .bootstrap.container import build_container
from .bootstrap.lifespan import lifespan
def create_app() -> FastAPI:
    app=FastAPI(title="教师教育智能体",version="0.1.0",lifespan=lifespan)
    app.state.container=build_container(); app.include_router(router)
    return app
app=create_app()
