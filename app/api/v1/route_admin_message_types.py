"""后台消息类型管理接口
更新日期: 2025-12-05
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_admin, get_db
from app.schemas.common import Page
from app.schemas.message_type import MessageTypeCreate, MessageTypeOut, MessageTypeUpdate
from app.services.admin.message_type_service import MessageTypeService
from app.core.response import success

router = APIRouter(prefix="/admin/message-types")


@router.get("", response_model=None)
async def list_message_types(
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> Page[MessageTypeOut]:
    service = MessageTypeService(db)
    return success(await service.list_message_types(page, page_size))


@router.post("", response_model=None)
async def create_message_type(
    payload: MessageTypeCreate,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> MessageTypeOut:
    service = MessageTypeService(db)
    return success(await service.create_message_type(payload))


@router.put("/{type_id}", response_model=None)
async def update_message_type(
    type_id: int,
    payload: MessageTypeUpdate,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> MessageTypeOut:
    service = MessageTypeService(db)
    return success(await service.update_message_type(type_id, payload))
