"""后台角色管理接口
更新日期: 2025-12-05
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_admin, get_db
from app.schemas.common import Page
from app.schemas.role import RoleCreate, RoleOut, RoleUpdate
from app.services.admin.admin_service import RoleService
from app.core.response import success

router = APIRouter(prefix="/admin/roles")


@router.get("/", response_model=None)
async def list_roles(
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> Page[RoleOut]:
    service = RoleService(db)
    return success(await service.list_roles(page, page_size))


@router.post("/", response_model=None)
async def create_role(
    payload: RoleCreate,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> RoleOut:
    service = RoleService(db)
    return success(await service.create_role(payload))


@router.put("/{role_id}", response_model=None)
async def update_role(
    role_id: int,
    payload: RoleUpdate,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> RoleOut:
    service = RoleService(db)
    return success(await service.update_role(role_id, payload))
