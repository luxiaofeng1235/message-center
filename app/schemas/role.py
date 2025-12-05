from datetime import datetime

from pydantic import BaseModel


class RoleCreate(BaseModel):
    name: str
    code: str
    description: str | None = None


class RoleUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class RoleOut(BaseModel):
    id: int
    name: str
    code: str
    description: str | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True
