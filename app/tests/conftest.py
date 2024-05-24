import json

import pytest
from database import REDIS_URL
from httpx import ASGITransport, AsyncClient
from redis import asyncio as aioredis

from app.config import settings
from app.main import app as fatapi_app


def open_mock_json(model: str):
    with open(f"app/tests/{model}", encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"
    redis = aioredis.from_url(
        url=REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
    )
    data: list = open_mock_json("mock_data.json")
    await redis.mset(data)
    await redis.aclose()


@pytest.fixture(scope="function")
async def redis_session():
    assert settings.MODE == "TEST"
    redis = aioredis.from_url(
        url=REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
    )
    yield redis
    await redis.aclose()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(
        transport=ASGITransport(app=fatapi_app), base_url="http://test"
    ) as client:
        yield client
