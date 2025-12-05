from datetime import datetime

from pydantic import BaseModel, Field


class MessageTypeCreate(BaseModel):
    code: str = Field(min_length=1)
    name: str = Field(min_length=1)
    description: str | None = None
    is_active: bool = True


class MessageTypeUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class MessageTypeOut(BaseModel):
    id: int
    code: str
    name: str
    description: str | None = None
    is_active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
