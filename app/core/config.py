from typing import Literal

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseModel):
    name: str = "Somna"
    version: str = "1.0.0"


class LoggingSettings(BaseModel):
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "DEBUG"
    format: str = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )


class DatabaseSettings(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    pool_timeout: int = 30
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class JWTSettings(BaseModel):
    algorithm: str = "HS256"
    secret_key: str
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7


class RedisSettings(BaseModel):
    host: str = "localhost"
    port: int = 6379
    max_connections: int = 10
    timeout: int = 5
    db_cache: int = 0
    db_auth: int = 1


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
    )

    app: AppSettings = AppSettings()
    logger: LoggingSettings = LoggingSettings()
    database: DatabaseSettings
    jwt: JWTSettings
    redis: RedisSettings = RedisSettings()


settings = Settings()
