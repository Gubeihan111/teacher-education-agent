"""Teacher education API."""
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .api.v1.router import router
from .bootstrap.container import build_container
from .bootstrap.lifespan import lifespan
def create_app() -> FastAPI:
    app=FastAPI(title="教师教育智能体",version="0.1.0",lifespan=lifespan)
    app.state.container=build_container(); app.include_router(router)
    web_root = Path(__file__).resolve().parents[2] / "web"
    if (web_root / "index.html").is_file():
        app.mount("/web", StaticFiles(directory=web_root), name="web")

        @app.get("/", include_in_schema=False)
        async def web_index():
            return FileResponse(web_root / "index.html", headers={"Cache-Control": "no-cache"})
    return app
app=create_app()
