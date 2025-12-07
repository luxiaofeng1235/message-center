"""后台路由聚合"""

from fastapi import APIRouter

from app.api.admin import (
    route_admin_apps,
    route_admin_auth,
    route_admin_channel_message_types,
    route_admin_channels,
    route_admin_message_types,
    route_admin_roles,
    route_admin_subscriptions,
    route_admin_templates,
    route_admin_user_mappings,
    route_admin_user_roles,
    route_admin_users,
    route_visitors,
)

router = APIRouter()
router.include_router(route_admin_auth.router, tags=["admin-auth"])
router.include_router(route_admin_users.router, tags=["admin-users"])
router.include_router(route_admin_roles.router, tags=["admin-roles"])
router.include_router(route_admin_apps.router, tags=["admin-apps"])
router.include_router(route_admin_channels.router, tags=["admin-channels"])
router.include_router(route_admin_channel_message_types.router, tags=["admin-channel-message-types"])
router.include_router(route_admin_message_types.router, tags=["admin-message-types"])
router.include_router(route_admin_templates.router, tags=["admin-message-templates"])
router.include_router(route_admin_subscriptions.router, tags=["admin-subscriptions"])
router.include_router(route_admin_user_roles.router, tags=["admin-user-roles"])
router.include_router(route_admin_user_mappings.router, tags=["admin-users"])
router.include_router(route_visitors.router, tags=["admin-visitors"])
