"""Redis 消费者：订阅消息并推送 WebSocket
更新日期: 2025-12-05
"""

import asyncio
import json
from datetime import datetime

from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.websocket.connection_manager import manager
from app.db.session import async_session
from app.models.message import Message
from app.models.message_delivery import MessageDelivery
from app.utils.redis import pattern_subscribe


async def _send_delivery(db: AsyncSession, delivery: MessageDelivery, message: Message) -> None:
    if not manager.is_online(delivery.user_id):
        return
    await manager.send_personal_message(
        delivery.user_id,
        json.dumps(
            {
                "delivery_id": delivery.id,
                "message_id": message.id,
                "title": message.title,
                "content": message.content,
                "payload": message.payload,
            }
        ),
    )
    await db.execute(
        update(MessageDelivery)
        .where(MessageDelivery.id == delivery.id)
        .values(status=1, sent_at=datetime.utcnow(), retry_count=delivery.retry_count)
    )
    await db.commit()


async def handle_message(db: AsyncSession, raw: str) -> None:
    payload = json.loads(raw)
    message_id = payload.get("message_id")
    dispatch_mode = payload.get("dispatch_mode", 0)
    user_ids = payload.get("user_ids", [])
    target_user_ids = payload.get("target_user_ids") or []
    message = await db.get(Message, message_id)
    if not message:
        return
    if dispatch_mode == 1:
        target_list = target_user_ids
    else:
        target_list = user_ids
    for uid in target_list:
        delivery = await db.scalar(
            select(MessageDelivery).where(
                and_(MessageDelivery.user_id == uid, MessageDelivery.message_id == message_id)
            )
        )
        if not delivery:
            continue
        try:
            await _send_delivery(db, delivery, message)
        except Exception as exc:  # noqa: BLE001
            await db.execute(
                update(MessageDelivery)
                .where(MessageDelivery.id == delivery.id)
                .values(
                    status=3,
                    last_error=str(exc),
                    retry_count=delivery.retry_count + 1,
                )
            )
            await db.commit()


async def resend_pending(interval: float = 5.0) -> None:
    """周期性扫描未发送/失败投递，重试推送在线用户。"""
    while True:
        async with async_session() as db:
            deliveries = await db.execute(
                select(MessageDelivery, Message)
                .join(Message, Message.id == MessageDelivery.message_id)
                .where(MessageDelivery.status.in_([0, 3]))
                .limit(100)
            )
            for delivery, message in deliveries.all():
                try:
                    await _send_delivery(db, delivery, message)
                except Exception as exc:  # noqa: BLE001
                    await db.execute(
                        update(MessageDelivery)
                        .where(MessageDelivery.id == delivery.id)
                        .values(
                            status=3,
                            last_error=str(exc),
                            retry_count=delivery.retry_count + 1,
                        )
                    )
                    await db.commit()
        await asyncio.sleep(interval)


async def run_consumer() -> None:
    async def consume():
        async for raw in pattern_subscribe("mc:channel:*"):
            async with async_session() as db:  # type: AsyncSession
                try:
                    await handle_message(db, raw)
                except Exception:
                    await asyncio.sleep(0.1)

    await asyncio.gather(consume(), resend_pending())


if __name__ == "__main__":
    asyncio.run(run_consumer())
