"""消息模板后台服务
更新日期: 2025-12-05
"""

from datetime import datetime
from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message_template import MessageTemplate
from app.schemas.common import Page, PageMeta
from app.schemas.message_template import MessageTemplateCreate, MessageTemplateOut, MessageTemplateUpdate
from app.utils.common import paginate_params


class TemplateService:
    """模板管理。"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_templates(
        self, page: int, page_size: int, app_id: int | None = None, channel_id: int | None = None
    ) -> Page[MessageTemplateOut]:
        offset, limit = paginate_params(page, page_size)
        stmt = select(MessageTemplate)
        count_stmt = select(func.count()).select_from(MessageTemplate)
        if app_id is not None:
            stmt = stmt.where(MessageTemplate.app_id == app_id)
            count_stmt = count_stmt.where(MessageTemplate.app_id == app_id)
        if channel_id is not None:
            stmt = stmt.where(MessageTemplate.channel_id == channel_id)
            count_stmt = count_stmt.where(MessageTemplate.channel_id == channel_id)
        total = await self.db.scalar(count_stmt)
        result = await self.db.execute(stmt.order_by(MessageTemplate.id.desc()).offset(offset).limit(limit))
        items: Sequence[MessageTemplate] = result.scalars().all()
        items_out = [MessageTemplateOut.model_validate(i, from_attributes=True) for i in items]
        return Page(meta=PageMeta(total=total or 0, page=page, page_size=page_size), items=items_out)

    async def create_template(self, data: MessageTemplateCreate) -> MessageTemplateOut:
        exists = await self.db.scalar(select(MessageTemplate).where(MessageTemplate.template_key == data.template_key))
        if exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Template key exists")
        tpl = MessageTemplate(
            app_id=data.app_id,
            channel_id=data.channel_id,
            template_key=data.template_key,
            name=data.name,
            title_template=data.title_template,
            content_template=data.content_template,
            payload_template=data.payload_template,
            is_default=data.is_default,
        )
        self.db.add(tpl)
        await self.db.commit()
        await self.db.refresh(tpl)
        return MessageTemplateOut.model_validate(tpl, from_attributes=True)

    async def update_template(self, template_id: int, data: MessageTemplateUpdate) -> MessageTemplateOut:
        result = await self.db.execute(select(MessageTemplate).where(MessageTemplate.id == template_id))
        tpl = result.scalar_one_or_none()
        if not tpl:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template not found")
        if data.name is not None:
            tpl.name = data.name
        if data.title_template is not None:
            tpl.title_template = data.title_template
        if data.content_template is not None:
            tpl.content_template = data.content_template
        if data.payload_template is not None:
            tpl.payload_template = data.payload_template
        if data.is_default is not None:
            tpl.is_default = data.is_default
        tpl.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(tpl)
        return MessageTemplateOut.model_validate(tpl, from_attributes=True)
