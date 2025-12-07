"""访客/在线连接查询接口"""

from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import and_, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.response import success
from app.models.client_connection import ClientConnection
from app.models.user import User
from app.schemas.client_connection import ClientConnectionOut

router = APIRouter(prefix="/visitors")


@router.get("", response_model=None)
async def list_visitors(
    app_id: int | None = None,
    role: str | None = None,
    start_time: datetime | None = None,
    end_time: datetime | None = None,
    limit: int = 500,
    db: AsyncSession = Depends(get_db),
) -> list[ClientConnectionOut]:
    """
    查询连接记录（可筛选 app、角色、在线状态、时间范围）。默认最多返回 500 条。
    """

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
    if start_time:
        conditions.append(ClientConnection.connected_at >= start_time)
    if end_time:
        conditions.append(ClientConnection.connected_at <= end_time)
    if conditions:
        stmt = stmt.where(and_(*conditions))

    result = await db.execute(stmt)
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
            )
        )
    return success(items)
