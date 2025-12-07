"""后台管理员用户接口
更新日期: 2025-12-05
"""

import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_admin, get_db
from app.schemas.admin import AdminCreate, AdminOut, AdminUpdate
from app.schemas.common import Page
from app.services.admin.admin_service import AdminService
from fastapi import HTTPException

from app.core.response import success, fail

router = APIRouter(prefix="/admin/users")
AVATAR_DIR = Path("public/avatar")
AVATAR_DIR.mkdir(parents=True, exist_ok=True)


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
    try:
        await service.deactivate_admin(admin_id, current_admin)
        return success({"status": "ok"})
    except HTTPException as exc:
        # 统一返回格式 code=0，便于前端识别
        return fail(exc.detail or "操作失败", status_code=exc.status_code)


@router.post("/avatar", response_model=None)
async def upload_avatar(
    file: UploadFile = File(...),
    _: object = Depends(get_current_admin),
):
    suffix = Path(file.filename).suffix or ".jpg"
    filename = f"{uuid.uuid4().hex}{suffix}"
    AVATAR_DIR.mkdir(parents=True, exist_ok=True)
    target = AVATAR_DIR / filename
    content = await file.read()
    target.write_bytes(content)
    url = f"/public/avatar/{filename}"
    return success({"url": url})
