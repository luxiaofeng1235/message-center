from datetime import datetime
from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models.admin_role import AdminRole
from app.models.admin_user import AdminUser
from app.schemas.admin import AdminCreate, AdminOut, AdminUpdate
from app.schemas.common import Page, PageMeta
from app.schemas.role import RoleCreate, RoleOut, RoleUpdate
from app.utils.common import paginate_params


class AdminService:
    """后台管理员相关服务：认证、增删改查、分页。"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def authenticate(self, username: str, password: str) -> AdminUser:
        result = await self.db.execute(select(AdminUser).where(AdminUser.username == username))
        user = result.scalar_one_or_none()
        if not user or not verify_password(password, user.password_hash) or not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="登录失败!")
        return user

    async def list_admins(self, page: int, page_size: int) -> Page[AdminOut]:
        offset, limit = paginate_params(page, page_size)
        total = await self.db.scalar(select(func.count()).select_from(AdminUser))
        result = await self.db.execute(
            select(AdminUser).order_by(AdminUser.id.desc()).offset(offset).limit(limit)
        )
        items: Sequence[AdminUser] = result.scalars().all()
        items_out = [AdminOut.model_validate(i, from_attributes=True) for i in items]
        return Page(meta=PageMeta(total=total or 0, page=page, page_size=page_size), items=items_out)

    async def create_admin(self, data: AdminCreate, current_admin: AdminUser) -> AdminOut:
        if not current_admin.is_super:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="仅超级管理员可创建账号")
        exists = await self.db.scalar(select(AdminUser).where(AdminUser.username == data.username))
        if exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username exists")
        admin = AdminUser(
            username=data.username,
            password_hash=get_password_hash(data.password),
            avatar=data.avatar,
            display_name=data.display_name,
            phone=data.phone,
            is_super=data.is_super,
            is_active=data.is_active,
        )
        self.db.add(admin)
        await self.db.commit()
        await self.db.refresh(admin)
        return AdminOut.model_validate(admin, from_attributes=True)

    async def update_admin(self, admin_id: int, data: AdminUpdate, current_admin: AdminUser) -> AdminOut:
        result = await self.db.execute(select(AdminUser).where(AdminUser.id == admin_id))
        admin = result.scalar_one_or_none()
        if not admin:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
        if admin.id == current_admin.id and (data.is_super is not None or data.is_active is not None):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="不能修改自身的启用/超管状态")
        if (data.is_super is not None or data.is_active is not None) and not current_admin.is_super:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="仅超级管理员可修改启用/超管状态")
        if data.display_name is not None:
            admin.display_name = data.display_name
        if data.phone is not None:
            admin.phone = data.phone
        if data.is_super is not None:
            admin.is_super = data.is_super
        if data.is_active is not None:
            admin.is_active = data.is_active
        if data.avatar is not None:
            admin.avatar = data.avatar
        if data.password:
            # 任何修改密码的操作都需提供原密码并校验
            if not data.old_password or not verify_password(data.old_password, admin.password_hash):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="旧密码错误")
            admin.password_hash = get_password_hash(data.password)
        admin.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(admin)
        return AdminOut.model_validate(admin, from_attributes=True)

    async def deactivate_admin(self, admin_id: int, current_admin: AdminUser) -> None:
        if admin_id == current_admin.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="不能禁用自己")
        if not current_admin.is_super:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="仅超级管理员可禁用账号")
        await self.db.execute(
            update(AdminUser).where(AdminUser.id == admin_id).values(is_active=False, updated_at=datetime.utcnow())
        )
        await self.db.commit()


class RoleService:
    """后台角色服务：角色分页/增改。"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_roles(self, page: int, page_size: int) -> Page[RoleOut]:
        offset, limit = paginate_params(page, page_size)
        total = await self.db.scalar(select(func.count()).select_from(AdminRole))
        result = await self.db.execute(
            select(AdminRole).order_by(AdminRole.id.desc()).offset(offset).limit(limit)
        )
        items: Sequence[AdminRole] = result.scalars().all()
        items_out = [RoleOut.model_validate(i, from_attributes=True) for i in items]
        return Page(meta=PageMeta(total=total or 0, page=page, page_size=page_size), items=items_out)

    async def create_role(self, data: RoleCreate) -> RoleOut:
        exists = await self.db.scalar(select(AdminRole).where(AdminRole.code == data.code))
        if exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role code exists")
        role = AdminRole(name=data.name, code=data.code, description=data.description)
        self.db.add(role)
        await self.db.commit()
        await self.db.refresh(role)
        return RoleOut.model_validate(role, from_attributes=True)

    async def update_role(self, role_id: int, data: RoleUpdate) -> RoleOut:
        result = await self.db.execute(select(AdminRole).where(AdminRole.id == role_id))
        role = result.scalar_one_or_none()
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
        if data.name is not None:
            role.name = data.name
        if data.description is not None:
            role.description = data.description
        await self.db.commit()
        await self.db.refresh(role)
        return RoleOut.model_validate(role, from_attributes=True)
