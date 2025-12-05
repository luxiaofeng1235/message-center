"""后台订阅管理接口
更新日期: 2025-12-05
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_admin, get_db
from app.schemas.channel import SubscriptionCreate, SubscriptionOut, SubscriptionUpdate
from app.schemas.common import Page
from app.services.admin.subscription_service import SubscriptionService
from app.core.response import success

router = APIRouter(prefix="/admin/subscriptions")


@router.get("/", response_model=None)
async def list_subscriptions(
    page: int = 1,
    page_size: int = 20,
    user_id: int | None = None,
    channel_id: int | None = None,
    message_type_id: int | None = None,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> Page[SubscriptionOut]:
    service = SubscriptionService(db)
    return success(
        await service.list_subscriptions(
            page, page_size, user_id=user_id, channel_id=channel_id, message_type_id=message_type_id
        )
    )


@router.post("/", response_model=None)
async def create_subscription(
    payload: SubscriptionCreate,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> SubscriptionOut:
    service = SubscriptionService(db)
    return success(await service.create_subscription(payload))


@router.put("/{subscription_id}", response_model=None)
async def update_subscription(
    subscription_id: int,
    payload: SubscriptionUpdate,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> SubscriptionOut:
    service = SubscriptionService(db)
    return success(await service.update_subscription(subscription_id, payload))
