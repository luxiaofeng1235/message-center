from datetime import datetime

from pydantic import BaseModel


class MessageCreate(BaseModel):
    app_id: int
    channel_id: int
    message_type_id: int
    title: str | None = None
    content: str
    payload: dict | None = None
    sender_user_id: str | None = None
    priority: int = 0
    message_key: str | None = None
    dispatch_mode: int | None = Field(default=None, ge=0, le=2)
    target_user_ids: list[int] | None = None


class MessageSendResponse(BaseModel):
    id: int
    created_at: datetime
    status: int
    message_key: str | None = None


class MessageOut(BaseModel):
    id: int
    app_id: int
    channel_id: int
    message_type_id: int
    title: str | None = None
    content: str
    payload: dict | None = None
    sender_user_id: str | None = None
    priority: int
    dispatch_mode: int
    target_user_ids: list[int] | None = None
    status: int
    message_key: str | None = None
    created_at: datetime | None = None
    published_at: datetime | None = None

    class Config:
        from_attributes = True
