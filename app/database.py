from typing import AsyncIterator

from redis import Redis
from redis import asyncio as aioredis

from app.config import settings

REDIS_URL = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"

if settings.MODE == "TEST":
    REDIS_URL = f"redis://{settings.TEST_REDIS_HOST}:{settings.TEST_REDIS_PORT}"


async def init_redis_pool() -> AsyncIterator[Redis]:
    session = aioredis.from_url(
        url=REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
    )
    yield session
    await session.aclose()
