import asyncio
import json

import redis.asyncio as redis

from app.core.config import get_settings

_settings = get_settings()
_redis: redis.Redis | None = None


def get_redis() -> redis.Redis:
    global _redis
    if _redis is None:
        _redis = redis.from_url(str(_settings.redis_url), decode_responses=True)
    return _redis


async def publish(channel: str, message: str) -> None:
    client = get_redis()
    await client.publish(channel, message)


async def subscribe(channel: str):
    client = get_redis()
    pubsub = client.pubsub()
    await pubsub.subscribe(channel)
    async for msg in pubsub.listen():
        if msg["type"] == "message":
            yield msg["data"]
    await pubsub.close()


async def pattern_subscribe(pattern: str):
    client = get_redis()
    pubsub = client.pubsub()
    await pubsub.psubscribe(pattern)
    async for msg in pubsub.listen():
        if msg["type"] == "pmessage":
            yield msg["data"]
    await pubsub.close()


async def close_redis() -> None:
    client = get_redis()
    await client.close()
