from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_admin, get_db
from app.schemas.admin import AdminLogin, AdminOut, AdminUpdate
from app.services.admin.admin_service import AdminService
from app.services.admin.auth_service import AuthService
from app.core.response import success, fail

router = APIRouter(prefix="/admin/auth")


@router.post("/login", response_model=None)
async def login(payload: AdminLogin, request: Request, db: AsyncSession = Depends(get_db)):
    service = AuthService(AdminService(db))
    client_ip = request.client.host if request.client else None
    try:
        token = await service.login(payload.username, payload.password, request_ip=client_ip)
        return success(token)
    except HTTPException as exc:
        return fail(exc.detail or "登录失败", status_code=200)


@router.get("/me", response_model=None)
async def me(current_admin=Depends(get_current_admin)) -> AdminOut:
    return success(AdminOut.model_validate(current_admin, from_attributes=True))


@router.put("/profile", response_model=None)
async def update_profile(
    payload: AdminUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    service = AdminService(db)
    return success(await service.update_admin(current_admin.id, payload, current_admin))
