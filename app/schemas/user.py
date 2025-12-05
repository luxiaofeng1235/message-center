from datetime import datetime

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    app_id: int
    external_user_id: str = Field(min_length=1)
    nickname: str | None = None


class UserOut(BaseModel):
    id: int
    app_id: int
    external_user_id: str
    nickname: str | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True
