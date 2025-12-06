from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.admin_user_role import AdminUserRole
from app.schemas.admin_user_role import AdminUserRoleCreate, AdminUserRoleOut
from app.schemas.common import Page, PageMeta
from app.utils.common import paginate_params


class AdminUserRoleService:
    """后台管理员-角色关系服务。"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_items(self, page: int, page_size: int, user_id: int | None = None) -> Page[AdminUserRoleOut]:
        offset, limit = paginate_params(page, page_size)
        stmt = select(AdminUserRole)
        count_stmt = select(func.count()).select_from(AdminUserRole)
        if user_id is not None:
            stmt = stmt.where(AdminUserRole.user_id == user_id)
            count_stmt = count_stmt.where(AdminUserRole.user_id == user_id)
        total = await self.db.scalar(count_stmt)
        result = await self.db.execute(stmt.order_by(AdminUserRole.id.desc()).offset(offset).limit(limit))
        items: Sequence[AdminUserRole] = result.scalars().all()
        items_out = [AdminUserRoleOut.model_validate(i, from_attributes=True) for i in items]
        return Page(meta=PageMeta(total=total or 0, page=page, page_size=page_size), items=items_out)

    async def create_item(self, data: AdminUserRoleCreate) -> AdminUserRoleOut:
        exists = await self.db.scalar(
            select(AdminUserRole).where(
                and_(AdminUserRole.user_id == data.user_id, AdminUserRole.role_id == data.role_id)
            )
        )
        if exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mapping exists")
        item = AdminUserRole(user_id=data.user_id, role_id=data.role_id)
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return AdminUserRoleOut.model_validate(item, from_attributes=True)

    async def delete_item(self, item_id: int) -> None:
        result = await self.db.execute(select(AdminUserRole).where(AdminUserRole.id == item_id))
        item = result.scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mapping not found")
        await self.db.delete(item)
        await self.db.commit()
