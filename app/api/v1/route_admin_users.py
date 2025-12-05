"""后台管理员用户接口
更新日期: 2025-12-05
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_admin, get_db
from app.schemas.admin import AdminCreate, AdminOut, AdminUpdate
from app.schemas.common import Page
from app.services.admin.admin_service import AdminService
from app.core.response import success

router = APIRouter(prefix="/admin/users")


@router.get("", response_model=None)
async def list_admins(
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> Page[AdminOut]:
    service = AdminService(db)
    return success(await service.list_admins(page, page_size))


@router.post("", response_model=None)
async def create_admin(
    payload: AdminCreate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
) -> AdminOut:
    service = AdminService(db)
    return success(await service.create_admin(payload, current_admin))


@router.put("/{admin_id}", response_model=None)
async def update_admin(
    admin_id: int,
    payload: AdminUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
) -> AdminOut:
    service = AdminService(db)
    return success(await service.update_admin(admin_id, payload, current_admin))


@router.delete("/{admin_id}")
async def deactivate_admin(
    admin_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
) -> dict[str, str]:
    service = AdminService(db)
    await service.deactivate_admin(admin_id, current_admin)
    return success({"status": "ok"})
