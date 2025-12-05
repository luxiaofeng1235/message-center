from datetime import datetime

from pydantic import BaseModel


class AppCreate(BaseModel):
    name: str
    code: str
    secret: str
    description: str | None = None
    is_active: bool = True


class AppUpdate(BaseModel):
    name: str | None = None
    secret: str | None = None
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
