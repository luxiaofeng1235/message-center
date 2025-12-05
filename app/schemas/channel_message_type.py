from datetime import datetime

from pydantic import BaseModel


class ChannelMessageTypeCreate(BaseModel):
    channel_id: int
    message_type_id: int
    is_default: bool = False
    config: dict | None = None
    is_active: bool = True


class ChannelMessageTypeUpdate(BaseModel):
    is_default: bool | None = None
    config: dict | None = None
    is_active: bool | None = None


class ChannelMessageTypeOut(BaseModel):
    id: int
    channel_id: int
    message_type_id: int
    is_default: bool
    config: dict | None = None
    is_active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
