from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.admin import AdminLogin
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
