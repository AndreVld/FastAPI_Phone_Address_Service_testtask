from typing import Annotated

from fastapi import Depends
from redis import Redis

from app.database import init_redis_pool
from app.logger import logger


class Service:
    def __init__(self, redis: Annotated[Redis, Depends(init_redis_pool)]) -> None:
        self._redis = redis

    async def write_address(self, phone: int, address: str):
        try:
            if await self.exists(phone):
                return "exists"
            await self._redis.set(phone, address)
        except Exception:
            extra = {
                "param": {
                    "phone": phone,
                    "address": address,
                }
            }
            logger.error(
                "An error occurred while recording data",
                exc_info=True,
                extra=extra,
            )
            return "error"

    async def exists(self, phone: int):
        try:
            return await self._redis.exists(phone)
        except Exception:
            extra = {
                "param": {
                    "phone": phone,
                }
            }
            logger.error(
                "Error checking the existence of key in database",
                exc_info=True,
                extra=extra,
            )

    async def rewrite_address(self, phone: int, address: str):
        try:
            await self._redis.set(phone, address)
            return True
        except Exception:
            extra = {
                "param": {
                    "phone": phone,
                    "address": address,
                }
            }
            logger.error(
                "An error occurred while overwriting data",
                exc_info=True,
                extra=extra,
            )
            return False

    async def get_address_by_phone(self, phone: int) -> str | None:
        try:
            return await self._redis.get(phone)
        except Exception:
            extra = {
                "param": {
                    "phone": phone,
                }
            }
            logger.error(
                "Error when trying to get a record by key from database",
                exc_info=True,
                extra=extra,
            )
