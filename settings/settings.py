from enum import StrEnum
import logging

from pydantic_settings import BaseSettings


class EnvType(StrEnum):
    """Environment type."""

    DEV = "dev"
    PROD = "prod"


class Settings(BaseSettings):
    app_name: str = "sejm-etl"
    env: EnvType = EnvType.DEV
    log_level: int = logging.INFO
    requests_external_timeout: int = 10

    number_of_years_to_process: int = 3
    cache_base_dir: str = f"/tmp/{app_name}/{str(env)}"


settings = Settings()


def get_settings() -> Settings:
    return settings
