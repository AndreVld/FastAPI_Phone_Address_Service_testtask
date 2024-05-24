from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING"]

    REDIS_HOST: str
    REDIS_PORT: int

    TEST_REDIS_HOST: str
    TEST_REDIS_PORT: int

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
