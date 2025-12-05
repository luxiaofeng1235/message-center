from datetime import datetime

from pydantic import BaseModel, Field


class AppCreate(BaseModel):
    name: str = Field(min_length=1)
    code: str = Field(min_length=1)
    secret: str = Field(min_length=1)
    description: str | None = None
    is_active: bool = True


class AppUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    secret: str | None = Field(default=None, min_length=1)
    description: str | None = None
    is_active: bool | None = None


class AppOut(BaseModel):
    id: int
    name: str
    code: str
    secret: str
    description: str | None = None
    is_active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
