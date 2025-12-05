"""业务消息接口
更新日期: 2025-12-05
"""

from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.common import Page
from app.schemas.message import MessageCreate, MessageOut, MessageSendResponse
from app.schemas.message_delivery import MessageDeliveryOut
from app.services.api.message_service import MessageService

router = APIRouter(prefix="/messages")


@router.post("/", response_model=MessageSendResponse)
async def send_message(
    payload: MessageCreate,
    db: AsyncSession = Depends(get_db),
    app_secret: str | None = Header(default=None, convert_underscores=False, alias="X-App-Secret"),
) -> MessageSendResponse:
    service = MessageService(db)
    return await service.send_message(payload, app_secret=app_secret)


@router.get("/", response_model=Page[MessageOut])
async def list_messages(
    page: int = 1,
    page_size: int = 20,
    app_id: int | None = None,
    channel_id: int | None = None,
    db: AsyncSession = Depends(get_db),
) -> Page[MessageOut]:
    service = MessageService(db)
    return await service.list_messages(page, page_size, app_id=app_id, channel_id=channel_id)


@router.get("/deliveries", response_model=Page[MessageDeliveryOut])
async def list_deliveries(
    page: int = 1,
    page_size: int = 20,
    user_id: int | None = None,
    status: int | None = None,
    db: AsyncSession = Depends(get_db),
) -> Page[MessageDeliveryOut]:
    service = MessageService(db)
    return await service.list_deliveries(page, page_size, user_id=user_id, status=status)
