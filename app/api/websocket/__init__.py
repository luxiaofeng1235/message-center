"""WebSocket 入口
更新日期: 2025-12-05
"""

import asyncio
import json
from collections import deque
from datetime import datetime
import uuid

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.websocket.connection_manager import manager
from app.db.session import async_session
from app.models.app import App
from app.models.channel import Channel
from app.models.client_connection import ClientConnection
from app.models.message import Message
from app.models.message_delivery import MessageDelivery
from app.models.subscription import Subscription
from app.models.user import User

router = APIRouter()

# 基础防护参数
MAX_TEXT_BYTES = 1_000_000  # ~1MB
RATE_WINDOW_SECONDS = 10
RATE_MAX_MESSAGES = 40
HEARTBEAT_TIMEOUT = 60  # 没有心跳/消息则超时关闭


@router.websocket("")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """
    处理客户端连接；要求 query 中包含 user_id、app_id、channel_id、instance_id、token。
    收到 {"delivery_id": int, "status": int} 视为 ACK。
    """

    external_user_id = websocket.query_params.get("external_user_id")
    client_id = websocket.query_params.get("client_id")
    instance_id = websocket.query_params.get("instance_id")
    app_id = websocket.query_params.get("app_id")
    channel_id = websocket.query_params.get("channel_id")
    token = websocket.query_params.get("token")
    role = websocket.query_params.get("role")
    try:
        iid = int(instance_id)
        aid = int(app_id)
        cid = int(channel_id)
    except (TypeError, ValueError):
        await websocket.close(code=1008)
        return
    # external_user_id 允许为空时用 token 代替
    external_identity = external_user_id or token
    if not external_identity or not iid or not aid or not cid or not token:
        await websocket.close(code=1008)
        return

    # 连接期查询与校验保持在同一会话
    async with async_session() as db:  # type: AsyncSession
        # 校验 App
        app_obj = await db.get(App, aid)
        if not app_obj or not app_obj.is_active:
            await websocket.close(code=1008)
            return
        if getattr(app_obj, "mode", 0) == 1:
            if role not in {"admin", "visitor"}:
                await websocket.close(code=1008)
                return

        # 校验 Channel
        channel = await db.get(Channel, cid)
        if not channel or not channel.is_active or channel.app_id != aid:
            await websocket.close(code=1008)
            return

        # 获取/创建内部用户（业务端无需传内部 user_id）
        user = await db.scalar(
            select(User).where(User.app_id == aid, User.external_user_id == external_identity)
        )
        if not user:
            user = User(app_id=aid, external_user_id=external_identity, nickname=None)
            db.add(user)
            await db.flush()
        uid = user.id

        # 订阅模式下，要求用户已订阅该通道
        if getattr(channel, "dispatch_mode", 0) == 0:
            sub_exists = await db.scalar(
                select(Subscription.id).where(
                    Subscription.user_id == uid,
                    Subscription.channel_id == cid,
                    Subscription.is_active.is_(True),
                )
            )
            if not sub_exists:
                await websocket.close(code=1008)
                return

        # 自动生成 client_id（若未传）
        client_id = client_id or f"cid_{uuid.uuid4().hex}"

        await manager.connect(uid, websocket)

        # 单用户保持一条记录：如已存在则更新状态，否则插入
        existing_conn = await db.scalar(select(ClientConnection).where(ClientConnection.user_id == uid))
        now_ts = datetime.utcnow()
        if existing_conn:
            existing_conn.instance_id = iid
            existing_conn.client_id = client_id
            existing_conn.role = role
            existing_conn.token = token
            existing_conn.user_agent = websocket.headers.get("user-agent")
            existing_conn.ip = websocket.client.host if websocket.client else None
            existing_conn.connected_at = now_ts
            existing_conn.last_active_at = now_ts
            existing_conn.disconnected_at = None
        else:
            conn = ClientConnection(
                user_id=uid,
                instance_id=iid,
                client_id=client_id,
                role=role,
                token=token,
                user_agent=websocket.headers.get("user-agent"),
                ip=websocket.client.host if websocket.client else None,
                connected_at=now_ts,
                last_active_at=now_ts,
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

        rate_window: deque[float] = deque()
        try:
            await websocket.send_text(json.dumps({"event": "connected", "client_id": client_id}))
            while True:
                try:
                    data = await asyncio.wait_for(websocket.receive_text(), timeout=HEARTBEAT_TIMEOUT)
                except asyncio.TimeoutError:
                    await websocket.close(code=1008)
                    break

                # 大小限制
                if len(data.encode("utf-8")) > MAX_TEXT_BYTES:
                    await websocket.send_text(json.dumps({"event": "error", "code": "too_large"}))
                    await websocket.close(code=1009)
                    break

                # 简单频率限制
                now_ts = datetime.utcnow().timestamp()
                rate_window.append(now_ts)
                while rate_window and now_ts - rate_window[0] > RATE_WINDOW_SECONDS:
                    rate_window.popleft()
                if len(rate_window) > RATE_MAX_MESSAGES:
                    await websocket.send_text(json.dumps({"event": "error", "code": "rate_limited"}))
                    await websocket.close(code=1008)
                    break

                # 原始 ping（非 JSON）
                if data.strip().lower() == "ping":
                    await db.execute(
                        ClientConnection.__table__
                        .update()
                        .where(ClientConnection.user_id == uid)
                        .values(last_active_at=datetime.utcnow())
                    )
                    await db.commit()
                    await websocket.send_text("PONG")
                    continue

                try:
                    payload = json.loads(data)
                except json.JSONDecodeError:
                    await websocket.send_text(json.dumps({"event": "error", "code": "invalid_json"}))
                    continue

                # 更新活跃时间（无论是否业务消息/心跳）
                await db.execute(
                    ClientConnection.__table__
                    .update()
                    .where(ClientConnection.user_id == uid)
                    .values(last_active_at=datetime.utcnow())
                )
                await db.commit()

                # 心跳处理
                if (isinstance(payload, dict) and payload.get("type") == "ping") or (
                    isinstance(payload, str) and payload.strip().lower() == "ping"
                ):
                    await websocket.send_text("PONG")
                    continue

                delivery_id = payload.get("delivery_id") if isinstance(payload, dict) else None
                status_val = payload.get("status") if isinstance(payload, dict) else None
                if delivery_id is not None and status_val is not None:
                    delivery = await db.get(MessageDelivery, delivery_id)
                    if delivery and delivery.user_id == uid:
                        delivery.status = int(status_val)
                        if int(status_val) == 2:
                            delivery.ack_at = datetime.utcnow()
                        await db.commit()
        except WebSocketDisconnect:
            pass
        finally:
            manager.disconnect(uid, websocket)
            await db.execute(
                ClientConnection.__table__
                .update()
                .where(ClientConnection.user_id == uid)
                .values(disconnected_at=datetime.utcnow())
            )
            await db.commit()
