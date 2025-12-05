from functools import lru_cache

from pydantic import AnyUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Message Center"
    debug: bool = True

    mysql_dsn: str = "mysql+asyncmy://user:password@localhost:3306/message_center"
    redis_url: AnyUrl | str = "redis://localhost:6379/0"

    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_expires_minutes: int = 60 * 24

    # App authentication (HTTP/gRPC 调用方)
    app_secret_header: str = "X-App-Secret"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
