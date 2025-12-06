from pydantic import BaseModel
from datetime import datetime


class AdminUserRoleCreate(BaseModel):
    user_id: int
    role_id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None


class AdminUserRoleOut(BaseModel):
    id: int
    user_id: int
    role_id: int


    class Config:
        from_attributes = True
