from fastapi import APIRouter

from app.api.v1 import (
    route_health,
    route_messages,
    route_instances,
    route_visitors,
)

router = APIRouter()
router.include_router(route_messages.router, tags=["messages"])
router.include_router(route_instances.router, tags=["instances"])
router.include_router(route_visitors.router, tags=["visitors"])
router.include_router(route_health.router, tags=["health"])
