from datetime import datetime

from pydantic import BaseModel, Field


class ChannelCreate(BaseModel):
    app_id: int
    channel_key: str = Field(min_length=1)
    name: str = Field(min_length=1)
    description: str | None = None
    is_active: bool = True
    dispatch_mode: int = Field(default=0, ge=0, le=2, description="0=按订阅,1=广播在线,2=广播所有")
    broadcast_filter: dict | None = None


class ChannelUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    description: str | None = None
    is_active: bool | None = None
    dispatch_mode: int | None = Field(default=None, ge=0, le=2)
    broadcast_filter: dict | None = None


class ChannelOut(BaseModel):
    id: int
    app_id: int
    channel_key: str
    name: str
    description: str | None = None
    is_active: bool
    dispatch_mode: int
    broadcast_filter: dict | None = None
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
