from datetime import datetime

from pydantic import BaseModel, Field


class AdminLogin(BaseModel):
    username: str
    password: str


class AdminCreate(BaseModel):
    username: str
    password: str
    display_name: str | None = None
    phone: str | None = None
    is_super: bool = False
    is_active: bool = True


class AdminUpdate(BaseModel):
    display_name: str | None = None
    phone: str | None = None
    is_super: bool | None = None
    is_active: bool | None = None
    password: str | None = Field(default=None, description="如果需要重置密码")


class AdminOut(BaseModel):
    id: int
    username: str
    display_name: str | None = None
    phone: str | None = None
    is_super: bool
    is_active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
