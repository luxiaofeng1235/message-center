"""后台业务系统管理接口
更新日期: 2025-12-05
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_admin, get_db
from app.schemas.app import AppCreate, AppOut, AppUpdate
from app.schemas.common import Page
from app.services.api.app_service import AppService
from app.core.response import success

router = APIRouter(prefix="/admin/apps")


@router.get("", response_model=None)
async def list_apps(
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> Page[AppOut]:
    service = AppService(db)
    return success(await service.list_apps(page, page_size))


@router.post("", response_model=None)
async def create_app(
    payload: AppCreate,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> AppOut:
    service = AppService(db)
    return success(await service.create_app(payload))


@router.put("/{app_id}", response_model=None)
async def update_app(
    app_id: int,
    payload: AppUpdate,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> AppOut:
    service = AppService(db)
    return success(await service.update_app(app_id, payload))
