from datetime import datetime, timedelta

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int | None = None


def default_expiry(minutes: int) -> int:
    return int(timedelta(minutes=minutes).total_seconds())
