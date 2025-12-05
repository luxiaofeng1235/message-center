from datetime import datetime

from pydantic import BaseModel


class InstanceHeartbeat(BaseModel):
    instance_key: str
    host: str | None = None
    pid: int | None = None


class InstanceOut(BaseModel):
    id: int
    instance_key: str
    host: str | None = None
    pid: int | None = None
    started_at: datetime | None = None
    last_heartbeat: datetime | None = None
    is_active: bool

    class Config:
        from_attributes = True
