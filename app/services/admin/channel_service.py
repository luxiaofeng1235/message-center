"""通道及相关配置后台服务
更新日期: 2025-12-05
"""

from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.channel import Channel
from app.schemas.channel import ChannelCreate, ChannelOut, ChannelUpdate
from app.schemas.common import Page, PageMeta
from app.utils.common import paginate_params


class ChannelService:
    """通道管理：分页、创建、更新。"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_channels(self, page: int, page_size: int, app_id: int | None = None) -> Page[ChannelOut]:
        offset, limit = paginate_params(page, page_size)
        stmt = select(Channel)
        count_stmt = select(func.count()).select_from(Channel)
        if app_id is not None:
            stmt = stmt.where(Channel.app_id == app_id)
            count_stmt = count_stmt.where(Channel.app_id == app_id)
        total = await self.db.scalar(count_stmt)
        result = await self.db.execute(stmt.order_by(Channel.id.desc()).offset(offset).limit(limit))
        items: Sequence[Channel] = result.scalars().all()
        items_out = [ChannelOut.model_validate(i, from_attributes=True) for i in items]
        return Page(meta=PageMeta(total=total or 0, page=page, page_size=page_size), items=items_out)

    async def create_channel(self, data: ChannelCreate) -> Channel:
        exists = await self.db.scalar(
            select(Channel).where(and_(Channel.app_id == data.app_id, Channel.channel_key == data.channel_key))
        )
        if exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Channel key exists for app")
        channel = Channel(
            app_id=data.app_id,
            channel_key=data.channel_key,
            name=data.name,
            description=data.description,
            is_active=data.is_active,
        )
        self.db.add(channel)
        await self.db.commit()
        await self.db.refresh(channel)
        return channel

    async def update_channel(self, channel_id: int, data: ChannelUpdate) -> Channel:
        result = await self.db.execute(select(Channel).where(Channel.id == channel_id))
        channel = result.scalar_one_or_none()
        if not channel:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")
        if data.name is not None:
            channel.name = data.name
        if data.description is not None:
            channel.description = data.description
        if data.is_active is not None:
            channel.is_active = data.is_active
        await self.db.commit()
        await self.db.refresh(channel)
        return channel
