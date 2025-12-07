"""访客/在线连接查询接口"""

from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.response import success
from app.schemas.client_connection import ClientConnectionOut
from app.services.admin.visitor_service import VisitorService

router = APIRouter(prefix="/admin/visitors")


@router.get("", response_model=None)
async def list_visitors(
    app_id: int | None = None,
    role: str | None = None,
    token: str | None = None,
    start_time: datetime | None = None,
    end_time: datetime | None = None,
    limit: int = 500,
    db: AsyncSession = Depends(get_db),
) -> list[ClientConnectionOut]:
    """
    查询连接记录（可筛选 app、角色、token 前缀、时间范围）。默认最多返回 500 条。
    """
    service = VisitorService(db)
    return success(
        await service.list_visitors(
            app_id=app_id, role=role, token=token, start_time=start_time, end_time=end_time, limit=limit
        )
    )
