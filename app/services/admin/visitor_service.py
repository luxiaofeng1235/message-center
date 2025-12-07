"""
visitor_service.py

主要功能：访客/连接查询服务（后台使用，基于 mc_client_connection）。
------------------------------------------------------
作者: 团队/姓名
日期: 2025-12-06
版本: 1.0.0
"""

from datetime import datetime
from typing import List

from sqlalchemy import and_, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.client_connection import ClientConnection
from app.models.user import User
from app.schemas.client_connection import ClientConnectionOut


class VisitorService:
    """访客/连接查询服务。"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_visitors(
        self,
        app_id: int | None = None,
        role: str | None = None,
        token: str | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        limit: int = 500,
    ) -> List[ClientConnectionOut]:
        limit = max(1, min(limit, 1000))

        stmt = (
            select(ClientConnection, User.app_id)
            .join(User, User.id == ClientConnection.user_id)
            .order_by(desc(ClientConnection.connected_at))
            .limit(limit)
        )

        conditions = []
        if app_id is not None:
            conditions.append(User.app_id == app_id)
        if role:
            conditions.append(ClientConnection.role == role)
        if token:
            conditions.append(ClientConnection.token.like(f"{token}%"))
        if start_time:
            conditions.append(ClientConnection.connected_at >= start_time)
        if end_time:
            conditions.append(ClientConnection.connected_at <= end_time)

        if conditions:
            stmt = stmt.where(and_(*conditions))

        result = await self.db.execute(stmt)
        rows = result.all()

        items: list[ClientConnectionOut] = []
        for conn, app_id_value in rows:
            items.append(
                ClientConnectionOut(
                    id=conn.id,
                    user_id=conn.user_id,
                    instance_id=conn.instance_id,
                    client_id=conn.client_id,
                    role=conn.role,
                    user_agent=conn.user_agent,
                    ip=conn.ip,
                    connected_at=conn.connected_at,
                    last_active_at=conn.last_active_at,
                    disconnected_at=conn.disconnected_at,
                    app_id=app_id_value,
                    online=conn.disconnected_at is None,
                    token=conn.token,
                )
            )
        return items
