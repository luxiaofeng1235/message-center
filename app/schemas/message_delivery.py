from datetime import datetime

from pydantic import BaseModel


class MessageDeliveryOut(BaseModel):
    id: int
    message_id: int
    user_id: int
    instance_id: int | None = None
    client_connection_id: int | None = None
    status: int
    retry_count: int
    last_error: str | None = None
    created_at: datetime | None = None
    sent_at: datetime | None = None
    ack_at: datetime | None = None

    class Config:
        from_attributes = True
