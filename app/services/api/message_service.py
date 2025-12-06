"""业务消息发送/查询服务
更新日期: 2025-12-05
"""

import json
from datetime import datetime
from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.models.app import App
from app.models.channel import Channel
from app.models.channel_message_type import ChannelMessageType
from app.models.message_type import MessageType
from app.models.message import Message
from app.models.message_delivery import MessageDelivery
from app.models.subscription import Subscription
from app.schemas.common import Page, PageMeta
from app.schemas.message import MessageCreate, MessageOut, MessageSendResponse
from app.schemas.message_delivery import MessageDeliveryOut
from app.utils.common import paginate_params
from app.utils.redis import publish


class MessageService:
    """消息发送、入库、投递生成、列表查询。"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def _verify_app(self, app_id: int, app_secret: str | None) -> App:
        result = await self.db.execute(select(App).where(App.id == app_id))
        app = result.scalar_one_or_none()
        if not app or not app.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid app")
        if app_secret is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing app secret")
        if app.secret != app_secret:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid app secret")
        return app

    async def send_message(self, payload: MessageCreate, app_secret: str | None = None) -> MessageSendResponse:
        await self._verify_app(payload.app_id, app_secret)
        channel = await self.db.scalar(
            select(Channel).where(and_(Channel.id == payload.channel_id, Channel.app_id == payload.app_id))
        )
        if not channel or not channel.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Channel not available")
        # 校验消息类型存在、启用，并且通道已配置且启用
        mt = await self.db.scalar(select(MessageType).where(MessageType.id == payload.message_type_id))
        if not mt or not mt.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Message type invalid")
        mapping = await self.db.scalar(
            select(ChannelMessageType).where(
                and_(
                    ChannelMessageType.channel_id == payload.channel_id,
                    ChannelMessageType.message_type_id == payload.message_type_id,
                    ChannelMessageType.is_active.is_(True),
                )
            )
        )
        if not mapping:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Message type not allowed for channel")
        if payload.message_key:
            exists_key = await self.db.scalar(select(Message).where(Message.message_key == payload.message_key))
            if exists_key:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Duplicate message key")

        dispatch_mode = payload.dispatch_mode if payload.dispatch_mode is not None else getattr(channel, "dispatch_mode", 0)
        target_user_ids: list[int] = payload.target_user_ids or []
        if dispatch_mode == 1 and not target_user_ids:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="target_user_ids required for single")

        message = Message(
            app_id=payload.app_id,
            channel_id=payload.channel_id,
            message_type_id=payload.message_type_id,
            message_key=payload.message_key,
            title=payload.title,
            content=payload.content,
            payload=payload.payload,
            priority=payload.priority,
            dispatch_mode=dispatch_mode,
            target_user_ids=target_user_ids or None,
            status=0,
            created_at=datetime.utcnow(),
        )
        self.db.add(message)
        await self.db.flush()

        # 生成投递列表
        user_ids: list[int] = []
        if dispatch_mode == 1:
            user_ids = target_user_ids
        else:
            subs_result = await self.db.execute(
                select(Subscription.user_id).where(
                    and_(
                        Subscription.channel_id == payload.channel_id,
                        Subscription.is_active.is_(True),
                        Subscription.message_type_id == payload.message_type_id,
                    )
                )
            )
            user_ids = [row[0] for row in subs_result.all()]
        # 广播模式（2）如需脱离订阅，可在此扩展，例如查询全部用户

        deliveries: list[MessageDelivery] = []
        for uid in user_ids:
            deliveries.append(
                MessageDelivery(
                    message_id=message.id,
                    user_id=uid,
                    status=0,
                    retry_count=0,
                    created_at=datetime.utcnow(),
                )
            )
        if deliveries:
            self.db.add_all(deliveries)

        await self.db.commit()
        await self.db.refresh(message)

        # Publish to Redis channel
        settings = get_settings()
        channel_name = f"mc:channel:{channel.channel_key}"
        await publish(
            channel_name,
            json.dumps(
                {
                    "message_id": message.id,
                    "channel_id": payload.channel_id,
                    "app_id": payload.app_id,
                    "title": payload.title,
                    "content": payload.content,
                    "payload": payload.payload,
                    "priority": payload.priority,
                    "dispatch_mode": dispatch_mode,
                    "target_user_ids": target_user_ids,
                    "user_ids": user_ids,
                }
            ),
        )
        message.status = 1
        message.published_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(message)
        return MessageSendResponse(id=message.id, created_at=message.created_at, status=message.status)

    async def list_messages(
        self, page: int, page_size: int, app_id: int | None = None, channel_id: int | None = None
    ) -> Page[MessageOut]:
        offset, limit = paginate_params(page, page_size)
        stmt = select(Message)
        count_stmt = select(func.count()).select_from(Message)
        if app_id is not None:
            stmt = stmt.where(Message.app_id == app_id)
            count_stmt = count_stmt.where(Message.app_id == app_id)
        if channel_id is not None:
            stmt = stmt.where(Message.channel_id == channel_id)
            count_stmt = count_stmt.where(Message.channel_id == channel_id)
        total = await self.db.scalar(count_stmt)
        result = await self.db.execute(stmt.order_by(Message.id.desc()).offset(offset).limit(limit))
        items: Sequence[Message] = result.scalars().all()
        items_out = [MessageOut.model_validate(i, from_attributes=True) for i in items]
        return Page(meta=PageMeta(total=total or 0, page=page, page_size=page_size), items=items_out)

    async def list_deliveries(
        self, page: int, page_size: int, user_id: int | None = None, status: int | None = None
    ) -> Page[MessageDeliveryOut]:
        offset, limit = paginate_params(page, page_size)
        stmt = select(MessageDelivery)
        count_stmt = select(func.count()).select_from(MessageDelivery)
        if user_id is not None:
            stmt = stmt.where(MessageDelivery.user_id == user_id)
            count_stmt = count_stmt.where(MessageDelivery.user_id == user_id)
        if status is not None:
            stmt = stmt.where(MessageDelivery.status == status)
            count_stmt = count_stmt.where(MessageDelivery.status == status)
        total = await self.db.scalar(count_stmt)
        result = await self.db.execute(stmt.order_by(MessageDelivery.id.desc()).offset(offset).limit(limit))
        items: Sequence[MessageDelivery] = result.scalars().all()
        items_out = [MessageDeliveryOut.model_validate(i, from_attributes=True) for i in items]
        return Page(meta=PageMeta(total=total or 0, page=page, page_size=page_size), items=items_out)
