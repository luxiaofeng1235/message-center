from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.app import App
from app.schemas.app import AppCreate, AppOut, AppUpdate
from app.schemas.common import Page, PageMeta
from app.utils.common import paginate_params


class AppService:
    """业务接入系统管理/鉴权服务。"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_apps(self, page: int, page_size: int) -> Page[AppOut]:
        offset, limit = paginate_params(page, page_size)
        total = await self.db.scalar(select(func.count()).select_from(App))
        result = await self.db.execute(select(App).order_by(App.id.desc()).offset(offset).limit(limit))
        items: Sequence[App] = result.scalars().all()
        items_out = [AppOut.model_validate(i, from_attributes=True) for i in items]
        return Page(meta=PageMeta(total=total or 0, page=page, page_size=page_size), items=items_out)

    async def create_app(self, data: AppCreate) -> AppOut:
        exists = await self.db.scalar(select(App).where(App.code == data.code))
        if exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="App code exists")
        app = App(
            name=data.name,
            code=data.code,
            secret=data.secret,
            description=data.description,
            is_active=data.is_active,
        )
        self.db.add(app)
        await self.db.commit()
        await self.db.refresh(app)
        return AppOut.model_validate(app, from_attributes=True)

    async def update_app(self, app_id: int, data: AppUpdate) -> AppOut:
        result = await self.db.execute(select(App).where(App.id == app_id))
        app = result.scalar_one_or_none()
        if not app:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="App not found")
        if data.name is not None:
            app.name = data.name
        if data.secret is not None:
            app.secret = data.secret
        if data.description is not None:
            app.description = data.description
        if data.is_active is not None:
            app.is_active = data.is_active
        await self.db.commit()
        await self.db.refresh(app)
        return AppOut.model_validate(app, from_attributes=True)

    async def verify_app_secret(self, app_id: int, secret: str) -> App:
        result = await self.db.execute(select(App).where(App.id == app_id))
        app = result.scalar_one_or_none()
        if not app or not app.is_active or app.secret != secret:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid app credentials")
        return app
