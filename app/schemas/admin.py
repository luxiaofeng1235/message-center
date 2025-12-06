from datetime import datetime

from pydantic import BaseModel, Field


class AdminLogin(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class AdminCreate(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=6)
    avatar: str | None = None
    display_name: str | None = None
    phone: str | None = None
    is_super: bool = False
    is_active: bool = True


class AdminUpdate(BaseModel):
    display_name: str | None = None
    phone: str | None = None
    is_super: bool | None = None
    is_active: bool | None = None
    avatar: str | None = Field(default=None, description="头像地址，相对 /public 或完整 URL")
    password: str | None = Field(default=None, description="如果需要重置密码", min_length=6)
    old_password: str | None = Field(default=None, description="修改自身密码时必填", min_length=6)


class AdminOut(BaseModel):
    id: int
    username: str
    avatar: str | None = None
    display_name: str | None = None
    phone: str | None = None
    is_super: bool
    is_active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
