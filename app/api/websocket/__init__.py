"""WebSocket 入口
更新日期: 2025-12-05
"""

import json
from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.websocket.connection_manager import manager
from app.db.session import async_session
from app.models.client_connection import ClientConnection
from app.models.message import Message
from app.models.message_delivery import MessageDelivery

router = APIRouter()


@router.websocket("")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """
    处理客户端连接；要求 query 中包含 user_id，可选 client_id。
    收到 {"delivery_id": int, "status": int} 视为 ACK。
    """

    user_id = websocket.query_params.get("user_id")
    client_id = websocket.query_params.get("client_id")
    instance_id = websocket.query_params.get("instance_id")
    if not user_id or not instance_id:
        await websocket.close()
        return
    uid = int(user_id)
    iid = int(instance_id)
    await manager.connect(uid, websocket)

    async with async_session() as db:  # type: AsyncSession
        conn = ClientConnection(
            user_id=uid,
            instance_id=iid,
            client_id=client_id,
            user_agent=websocket.headers.get("user-agent"),
            ip=websocket.client.host if websocket.client else None,
            connected_at=datetime.utcnow(),
        )
        db.add(conn)
        await db.commit()
        # 补发未送达/失败的投递
        pending = await db.execute(
            select(MessageDelivery, Message)
            .join(Message, Message.id == MessageDelivery.message_id)
            .where(MessageDelivery.user_id == uid, MessageDelivery.status.in_([0, 3]))
            .limit(50)
        )
        for delivery, message in pending.all():
            await manager.send_personal_message(
                uid,
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
                MessageDelivery.__table__
                .update()
                .where(MessageDelivery.id == delivery.id)
                .values(status=1, sent_at=datetime.utcnow())
            )
            await db.commit()
    try:
        await websocket.send_text("connected")
        while True:
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
                delivery_id = payload.get("delivery_id")
                status = payload.get("status")
                if delivery_id is not None and status is not None:
                    async with async_session() as db:  # type: AsyncSession
                        delivery = await db.get(MessageDelivery, delivery_id)
                        if delivery and delivery.user_id == uid:
                            delivery.status = int(status)
                            if int(status) == 2:
                                delivery.ack_at = datetime.utcnow()
                            await db.commit()
            except json.JSONDecodeError:
                await websocket.send_text("invalid json")
    except WebSocketDisconnect:
        manager.disconnect(uid, websocket)
