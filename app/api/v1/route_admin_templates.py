"""后台消息模板管理接口
更新日期: 2025-12-05
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_admin, get_db
from app.schemas.common import Page
from app.schemas.message_template import MessageTemplateCreate, MessageTemplateOut, MessageTemplateUpdate
from app.services.admin.template_service import TemplateService
from app.core.response import success

router = APIRouter(prefix="/admin/templates")


@router.get("/", response_model=Page[MessageTemplateOut])
async def list_templates(
    page: int = 1,
    page_size: int = 20,
    app_id: int | None = None,
    channel_id: int | None = None,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> Page[MessageTemplateOut]:
    service = TemplateService(db)
    return success(await service.list_templates(page, page_size, app_id=app_id, channel_id=channel_id))


@router.post("/", response_model=MessageTemplateOut)
async def create_template(
    payload: MessageTemplateCreate,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> MessageTemplateOut:
    service = TemplateService(db)
    return success(await service.create_template(payload))


@router.put("/{template_id}", response_model=MessageTemplateOut)
async def update_template(
    template_id: int,
    payload: MessageTemplateUpdate,
    db: AsyncSession = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> MessageTemplateOut:
    service = TemplateService(db)
    return success(await service.update_template(template_id, payload))
