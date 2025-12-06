from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import deps  # noqa: F401  # side-effect imports for dependencies
from app.api.v1 import router as api_router
from app.api.websocket import router as ws_router
from app.core.response import success


def create_app() -> FastAPI:
    app = FastAPI(title="Message Center", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    static_dir = Path("public")
    static_dir.mkdir(parents=True, exist_ok=True)
    app.mount("/public", StaticFiles(directory=str(static_dir)), name="public")

    @app.get("/")
    async def root():
        return success({"service": "Message Center", "status": "ok"})
    app.include_router(api_router, prefix="/api/v1")
    app.include_router(ws_router, prefix="/ws")
    return app


app = create_app()


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}
