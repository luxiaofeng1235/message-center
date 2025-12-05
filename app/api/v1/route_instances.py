"""实例心跳接口
更新日期: 2025-12-05
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.instance import InstanceHeartbeat, InstanceOut
from app.services.ws.instance_service import InstanceService

router = APIRouter(prefix="/instances")


@router.post("/heartbeat", response_model=InstanceOut)
async def heartbeat(payload: InstanceHeartbeat, db: AsyncSession = Depends(get_db)) -> InstanceOut:
    service = InstanceService(db)
    return await service.heartbeat(payload)
