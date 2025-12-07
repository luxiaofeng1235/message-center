from fastapi import APIRouter

from app.api.v1 import router as v1_router
from app.admin import router as admin_router
from app.api.websocket import router as ws_router  # noqa: F401

router = APIRouter()
router.include_router(v1_router, prefix="/v1")
