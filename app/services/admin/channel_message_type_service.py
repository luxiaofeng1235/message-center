"""通道消息类型配置后台服务
更新日期: 2025-12-05
"""

from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.channel_message_type import ChannelMessageType
from app.schemas.channel_message_type import (
    ChannelMessageTypeCreate,
    ChannelMessageTypeOut,
    ChannelMessageTypeUpdate,
)
from app.schemas.common import Page, PageMeta
from app.utils.common import paginate_params


class ChannelMessageTypeService:
    """通道支持的消息类型配置。"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_items(
        self, page: int, page_size: int, channel_id: int | None = None
    ) -> Page[ChannelMessageType]:
        offset, limit = paginate_params(page, page_size)
        stmt = select(ChannelMessageType)
        count_stmt = select(func.count()).select_from(ChannelMessageType)
        if channel_id is not None:
            stmt = stmt.where(ChannelMessageType.channel_id == channel_id)
            count_stmt = count_stmt.where(ChannelMessageType.channel_id == channel_id)
        total = await self.db.scalar(count_stmt)
        result = await self.db.execute(stmt.order_by(ChannelMessageType.id.desc()).offset(offset).limit(limit))
        items: Sequence[ChannelMessageType] = result.scalars().all()
        return Page(meta=PageMeta(total=total or 0, page=page, page_size=page_size), items=items)

    async def create_item(self, data: ChannelMessageTypeCreate) -> ChannelMessageType:
        exists = await self.db.scalar(
            select(ChannelMessageType).where(
                and_(
                    ChannelMessageType.channel_id == data.channel_id,
                    ChannelMessageType.message_type_id == data.message_type_id,
                )
            )
        )
        if exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mapping exists")
        item = ChannelMessageType(
            channel_id=data.channel_id,
            message_type_id=data.message_type_id,
            is_default=data.is_default,
            config=data.config,
            is_active=data.is_active,
        )
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def update_item(self, item_id: int, data: ChannelMessageTypeUpdate) -> ChannelMessageType:
        result = await self.db.execute(select(ChannelMessageType).where(ChannelMessageType.id == item_id))
        item = result.scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mapping not found")
        if data.is_default is not None:
            item.is_default = data.is_default
        if data.config is not None:
            item.config = data.config
        if data.is_active is not None:
            item.is_active = data.is_active
        await self.db.commit()
        await self.db.refresh(item)
        return item
