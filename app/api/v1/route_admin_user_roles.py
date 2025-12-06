"""后台管理员-角色关系接口"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_admin, get_db
from app.core.response import success
from app.schemas.admin_user_role import AdminUserRoleCreate, AdminUserRoleOut
from app.schemas.common import Page
from app.services.admin.admin_user_role_service import AdminUserRoleService

router = APIRouter(prefix="/admin/user-roles")


@router.get("", response_model=None)
async def list_user_roles(
    page: int = 1,
    page_size: int = 20,
    user_id: int | None = None,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> Page[AdminUserRoleOut]:
    service = AdminUserRoleService(db)
    return success(await service.list_items(page, page_size, user_id=user_id))


@router.post("", response_model=None)
async def create_user_role(
    payload: AdminUserRoleCreate,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> AdminUserRoleOut:
    service = AdminUserRoleService(db)
    return success(await service.create_item(payload))


@router.delete("/{item_id}", response_model=None)
async def delete_user_role(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> dict[str, str]:
    service = AdminUserRoleService(db)
    await service.delete_item(item_id)
    return success({"status": "ok"})
