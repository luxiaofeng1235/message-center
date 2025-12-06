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
from app.models.channel import Channel
from app.models.app import App
from app.models.user import User
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
    app_id = websocket.query_params.get("app_id")
    channel_id = websocket.query_params.get("channel_id")
    token = websocket.query_params.get("token")
    role = websocket.query_params.get("role")
    try:
        uid = int(user_id)
        iid = int(instance_id)
        aid = int(app_id)
        cid = int(channel_id)
    except (TypeError, ValueError):
        await websocket.close(code=1008)
        return
    if not uid or not iid or not aid or not cid or not token:
        await websocket.close(code=1008)
        return
    await manager.connect(uid, websocket)

    async with async_session() as db:  # type: AsyncSession
        # 校验 App / Channel / User
        app_obj = await db.get(App, aid)
        if not app_obj or not app_obj.is_active:
            await websocket.close(code=1008)
            return
        if getattr(app_obj, "mode", 0) == 1:
            if not role:
                await websocket.close(code=1008)
                return
        channel = await db.get(Channel, cid)
        if not channel or not channel.is_active or channel.app_id != aid:
            await websocket.close(code=1008)
            return
        user = await db.get(User, uid)
        if not user or user.app_id != aid:
            await websocket.close(code=1008)
            return
        conn = ClientConnection(
            user_id=uid,
            instance_id=iid,
            client_id=client_id,
            role=role,
            token=token,
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
