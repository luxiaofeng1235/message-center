from fastapi import APIRouter

from app.api.v1 import (
    route_admin_apps,
    route_admin_auth,
    route_admin_channels,
    route_admin_channel_message_types,
    route_admin_message_types,
    route_admin_roles,
    route_admin_subscriptions,
    route_admin_templates,
    route_admin_users,
    route_admin_user_mappings,
    route_health,
    route_messages,
    route_instances,
)

router = APIRouter()
router.include_router(route_admin_auth.router, tags=["auth"])
router.include_router(route_admin_users.router, tags=["admin-users"])
router.include_router(route_admin_roles.router, tags=["roles"])
router.include_router(route_admin_apps.router, tags=["apps"])
router.include_router(route_admin_channels.router, tags=["channels"])
router.include_router(route_admin_channel_message_types.router, tags=["channel-message-types"])
router.include_router(route_admin_message_types.router, tags=["message-types"])
router.include_router(route_admin_templates.router, tags=["message-templates"])
router.include_router(route_admin_subscriptions.router, tags=["subscriptions"])
router.include_router(route_admin_user_mappings.router, tags=["users"])
router.include_router(route_messages.router, tags=["messages"])
router.include_router(route_instances.router, tags=["instances"])
router.include_router(route_health.router, tags=["health"])
