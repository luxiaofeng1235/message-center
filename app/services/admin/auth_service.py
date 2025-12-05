from datetime import datetime, timedelta

from app.core.config import get_settings
from app.core.security import create_access_token
from app.schemas.auth import Token
from app.services.admin.admin_service import AdminService


class AuthService:
    """后台登录认证服务。"""

    def __init__(self, admin_service: AdminService):
        self.admin_service = admin_service

    async def login(self, username: str, password: str, request_ip: str | None = None) -> Token:
        admin = await self.admin_service.authenticate(username, password)
        settings = get_settings()
        expires_delta = timedelta(minutes=settings.access_token_expires_minutes)
        token = create_access_token(subject=admin.username, expires_delta=expires_delta)
        # 更新最近登录信息
        try:
            admin.last_login_ip = request_ip
            admin.last_login_at = datetime.utcnow()
            await self.admin_service.db.commit()
        except Exception:
            await self.admin_service.db.rollback()
        return Token(access_token=token, expires_in=int(expires_delta.total_seconds()))
