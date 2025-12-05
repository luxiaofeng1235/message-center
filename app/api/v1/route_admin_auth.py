from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.admin import AdminLogin
from app.schemas.auth import Token
from app.services.admin.admin_service import AdminService
from app.services.admin.auth_service import AuthService
from app.core.response import success

router = APIRouter(prefix="/admin/auth")


@router.post("/login", response_model=Token)
async def login(payload: AdminLogin, request: Request, db: AsyncSession = Depends(get_db)) -> Token:
    service = AuthService(AdminService(db))
    client_ip = request.client.host if request.client else None
    token = await service.login(payload.username, payload.password, request_ip=client_ip)
    return success(token)
