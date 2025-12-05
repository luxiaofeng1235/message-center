from datetime import datetime

from pydantic import BaseModel


class MessageTemplateCreate(BaseModel):
    app_id: int
    channel_id: int | None = None
    template_key: str
    name: str
    title_template: str | None = None
    content_template: str
    payload_template: dict | None = None
    is_default: bool = False


class MessageTemplateUpdate(BaseModel):
    name: str | None = None
    title_template: str | None = None
    content_template: str | None = None
    payload_template: dict | None = None
    is_default: bool | None = None


class MessageTemplateOut(BaseModel):
    id: int
    app_id: int
    channel_id: int | None = None
    template_key: str
    name: str
    title_template: str | None = None
    content_template: str
    payload_template: dict | None = None
    is_default: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
