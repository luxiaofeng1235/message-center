"""后台通道管理接口
更新日期: 2025-12-05
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_admin, get_db
from app.schemas.channel import ChannelCreate, ChannelOut, ChannelUpdate
from app.schemas.common import Page
from app.services.admin.channel_service import ChannelService

router = APIRouter(prefix="/admin/channels")


@router.get("/", response_model=Page[ChannelOut])
async def list_channels(
    page: int = 1,
    page_size: int = 20,
    app_id: int | None = None,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> Page[ChannelOut]:
    service = ChannelService(db)
    return await service.list_channels(page, page_size, app_id=app_id)


@router.post("/", response_model=ChannelOut)
async def create_channel(
    payload: ChannelCreate,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> ChannelOut:
    service = ChannelService(db)
    return await service.create_channel(payload)


@router.put("/{channel_id}", response_model=ChannelOut)
async def update_channel(
    channel_id: int,
    payload: ChannelUpdate,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> ChannelOut:
    service = ChannelService(db)
    return await service.update_channel(channel_id, payload)
