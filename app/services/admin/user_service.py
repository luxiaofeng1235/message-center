"""业务用户后台服务
更新日期: 2025-12-05
"""

from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.common import Page, PageMeta
from app.schemas.user import UserCreate, UserOut
from app.utils.common import paginate_params


class UserService:
    """业务用户映射管理。"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_users(self, page: int, page_size: int, app_id: int | None = None) -> Page[UserOut]:
        offset, limit = paginate_params(page, page_size)
        stmt = select(User)
        count_stmt = select(func.count()).select_from(User)
        if app_id is not None:
            stmt = stmt.where(User.app_id == app_id)
            count_stmt = count_stmt.where(User.app_id == app_id)
        total = await self.db.scalar(count_stmt)
        result = await self.db.execute(stmt.order_by(User.id.desc()).offset(offset).limit(limit))
        items: Sequence[User] = result.scalars().all()
        items_out = [UserOut.model_validate(i, from_attributes=True) for i in items]
        return Page(meta=PageMeta(total=total or 0, page=page, page_size=page_size), items=items_out)

    async def create_user(self, data: UserCreate) -> User:
        exists = await self.db.scalar(
            select(User).where(and_(User.app_id == data.app_id, User.external_user_id == data.external_user_id))
        )
        if exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
        user = User(app_id=data.app_id, external_user_id=data.external_user_id, nickname=data.nickname)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
