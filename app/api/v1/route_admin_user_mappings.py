"""后台业务用户管理接口
更新日期: 2025-12-05
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_admin, get_db
from app.schemas.common import Page
from app.schemas.user import UserCreate, UserOut
from app.services.admin.user_service import UserService
from app.core.response import success

router = APIRouter(prefix="/admin/users-mapping")


@router.get("/", response_model=None)
async def list_users(
    page: int = 1,
    page_size: int = 20,
    app_id: int | None = None,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> Page[UserOut]:
    service = UserService(db)
    return success(await service.list_users(page, page_size, app_id=app_id))


@router.post("/", response_model=None)
async def create_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> UserOut:
    service = UserService(db)
    return success(await service.create_user(payload))
