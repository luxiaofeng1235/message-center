"""通道消息类型配置接口
更新日期: 2025-12-05
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_admin, get_db
from app.schemas.channel_message_type import (
    ChannelMessageTypeCreate,
    ChannelMessageTypeOut,
    ChannelMessageTypeUpdate,
)
from app.schemas.common import Page
from app.services.admin.channel_message_type_service import ChannelMessageTypeService
from app.core.response import success

router = APIRouter(prefix="/admin/channel-message-types")


@router.get("/", response_model=None)
async def list_items(
    page: int = 1,
    page_size: int = 20,
    channel_id: int | None = None,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> Page[ChannelMessageTypeOut]:
    service = ChannelMessageTypeService(db)
    return success(await service.list_items(page, page_size, channel_id=channel_id))


@router.post("/", response_model=ChannelMessageTypeOut)
async def create_item(
    payload: ChannelMessageTypeCreate,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> ChannelMessageTypeOut:
    service = ChannelMessageTypeService(db)
    return success(await service.create_item(payload))


@router.put("/{item_id}", response_model=ChannelMessageTypeOut)
async def update_item(
    item_id: int,
    payload: ChannelMessageTypeUpdate,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> ChannelMessageTypeOut:
    service = ChannelMessageTypeService(db)
    return success(await service.update_item(item_id, payload))
