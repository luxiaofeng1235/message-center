from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.admin import AdminLogin
from app.schemas.auth import Token
from app.services.admin.admin_service import AdminService
from app.services.admin.auth_service import AuthService

router = APIRouter(prefix="/admin/auth")


@router.post("/login", response_model=Token)
async def login(payload: AdminLogin, db: AsyncSession = Depends(get_db)) -> Token:
    service = AuthService(AdminService(db))
    return await service.login(payload.username, payload.password)
