"""消息类型后台服务
更新日期: 2025-12-05
"""

from datetime import datetime
from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message_type import MessageType
from app.schemas.common import Page, PageMeta
from app.schemas.message_type import MessageTypeCreate, MessageTypeOut, MessageTypeUpdate
from app.utils.common import paginate_params


class MessageTypeService:
    """消息类型管理。"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_message_types(self, page: int, page_size: int) -> Page[MessageTypeOut]:
        offset, limit = paginate_params(page, page_size)
        total = await self.db.scalar(select(func.count()).select_from(MessageType))
        result = await self.db.execute(
            select(MessageType).order_by(MessageType.id.desc()).offset(offset).limit(limit)
        )
        items: Sequence[MessageType] = result.scalars().all()
        items_out = [MessageTypeOut.model_validate(mt, from_attributes=True) for mt in items]
        return Page(meta=PageMeta(total=total or 0, page=page, page_size=page_size), items=items_out)

    async def create_message_type(self, data: MessageTypeCreate) -> MessageTypeOut:
        exists = await self.db.scalar(select(MessageType).where(MessageType.code == data.code))
        if exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Message type code exists")
        mt = MessageType(
            code=data.code,
            name=data.name,
            description=data.description,
            is_active=data.is_active,
        )
        self.db.add(mt)
        await self.db.commit()
        await self.db.refresh(mt)
        return MessageTypeOut.model_validate(mt, from_attributes=True)

    async def update_message_type(self, type_id: int, data: MessageTypeUpdate) -> MessageTypeOut:
        result = await self.db.execute(select(MessageType).where(MessageType.id == type_id))
        mt = result.scalar_one_or_none()
        if not mt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message type not found")
        if data.name is not None:
            mt.name = data.name
        if data.description is not None:
            mt.description = data.description
        if data.is_active is not None:
            mt.is_active = data.is_active
        mt.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(mt)
        return MessageTypeOut.model_validate(mt, from_attributes=True)
