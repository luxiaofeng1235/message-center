"""订阅后台服务
更新日期: 2025-12-05
"""

from datetime import datetime
from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.channel import Channel
from app.models.channel_message_type import ChannelMessageType
from app.models.subscription import Subscription
from app.schemas.channel import SubscriptionCreate, SubscriptionOut, SubscriptionUpdate
from app.schemas.common import Page, PageMeta
from app.utils.common import paginate_params


class SubscriptionService:
    """用户与通道订阅管理。"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_subscriptions(
        self,
        page: int,
        page_size: int,
        user_id: int | None = None,
        channel_id: int | None = None,
        message_type_id: int | None = None,
    ) -> Page[Subscription]:
        offset, limit = paginate_params(page, page_size)
        stmt = select(Subscription)
        count_stmt = select(func.count()).select_from(Subscription)
        if user_id is not None:
            stmt = stmt.where(Subscription.user_id == user_id)
            count_stmt = count_stmt.where(Subscription.user_id == user_id)
        if channel_id is not None:
            stmt = stmt.where(Subscription.channel_id == channel_id)
            count_stmt = count_stmt.where(Subscription.channel_id == channel_id)
        if message_type_id is not None:
            stmt = stmt.where(Subscription.message_type_id == message_type_id)
            count_stmt = count_stmt.where(Subscription.message_type_id == message_type_id)
        total = await self.db.scalar(count_stmt)
        result = await self.db.execute(stmt.order_by(Subscription.id.desc()).offset(offset).limit(limit))
        items: Sequence[Subscription] = result.scalars().all()
        items_out = [SubscriptionOut.model_validate(i, from_attributes=True) for i in items]
        return Page(meta=PageMeta(total=total or 0, page=page, page_size=page_size), items=items_out)

    async def create_subscription(self, data: SubscriptionCreate) -> SubscriptionOut:
        # 校验通道
        channel = await self.db.scalar(select(Channel).where(Channel.id == data.channel_id))
        if not channel or not channel.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Channel invalid")
        # 校验通道消息类型映射
        if data.message_type_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="message_type_id required")
        mapping = await self.db.scalar(
            select(ChannelMessageType).where(
                and_(
                    ChannelMessageType.channel_id == data.channel_id,
                    ChannelMessageType.message_type_id == data.message_type_id,
                    ChannelMessageType.is_active.is_(True),
                )
            )
        )
        if not mapping:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Message type not allowed for channel"
            )
        exists = await self.db.scalar(
            select(Subscription).where(
                and_(
                    Subscription.user_id == data.user_id,
                    Subscription.channel_id == data.channel_id,
                    Subscription.message_type_id == data.message_type_id,
                )
            )
        )
        if exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Subscription exists")
        sub = Subscription(
            user_id=data.user_id,
            channel_id=data.channel_id,
            message_type_id=data.message_type_id,
            is_active=data.is_active,
            source=data.source,
        )
        self.db.add(sub)
        await self.db.commit()
        await self.db.refresh(sub)
        return SubscriptionOut.model_validate(sub, from_attributes=True)

    async def update_subscription(self, subscription_id: int, data: SubscriptionUpdate) -> SubscriptionOut:
        result = await self.db.execute(select(Subscription).where(Subscription.id == subscription_id))
        sub = result.scalar_one_or_none()
        if not sub:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
        if data.is_active is not None:
            sub.is_active = data.is_active
        if data.source is not None:
            sub.source = data.source
        await self.db.commit()
        await self.db.refresh(sub)
        return SubscriptionOut.model_validate(sub, from_attributes=True)
