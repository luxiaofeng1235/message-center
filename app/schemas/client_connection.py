from datetime import datetime

from pydantic import BaseModel


class ClientConnectionOut(BaseModel):
    id: int
    user_id: int
    instance_id: int
    client_id: str | None = None
    role: str | None = None
    user_agent: str | None = None
    ip: str | None = None
    connected_at: datetime | None = None
    last_active_at: datetime | None = None
    disconnected_at: datetime | None = None
    app_id: int | None = None
    online: bool = False

    class Config:
        from_attributes = True
