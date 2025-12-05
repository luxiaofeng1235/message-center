from datetime import datetime

from pydantic import BaseModel, Field


class ChannelCreate(BaseModel):
    app_id: int
    channel_key: str = Field(min_length=1)
    name: str = Field(min_length=1)
    description: str | None = None
    is_active: bool = True


class ChannelUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    description: str | None = None
    is_active: bool | None = None


class ChannelOut(BaseModel):
    id: int
    app_id: int
    channel_key: str
    name: str
    description: str | None = None
    is_active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class SubscriptionCreate(BaseModel):
    user_id: int
    channel_id: int
    message_type_id: int
    is_active: bool = True
    source: int = 1


class SubscriptionUpdate(BaseModel):
    is_active: bool | None = None
    source: int | None = None


class SubscriptionOut(BaseModel):
    id: int
    user_id: int
    channel_id: int
    message_type_id: int
    is_active: bool
    source: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
