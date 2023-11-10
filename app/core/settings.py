from __future__ import annotations

from pydantic_settings import BaseSettings as PydanticBaseSettings
from pydantic_settings import SettingsConfigDict


class BaseSettings(PydanticBaseSettings):
    model_config = SettingsConfigDict(
        extra="allow",
        env_file=".env",
        env_file_encoding="utf-8",
    )


class ServerSettings(BaseSettings):
    DEBUG: bool
    RELOAD: bool
    HOSTNAME: str
    AUTH_PORT: int


server_settings = ServerSettings()


class LoggingSettings(BaseSettings):
    AUTH_MAIN_LOGGER_NAME: str
    LOGGING_LEVEL: str


logging_settings = LoggingSettings()


class DatabaseSettings(BaseSettings):
    DATABASE_DRIVER: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    AUTH_DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_NAME: str

    @property
    def url(self) -> str:
        driver, user, password, host, port, name = (
            self.DATABASE_DRIVER,
            self.DATABASE_USERNAME,
            self.DATABASE_PASSWORD,
            self.AUTH_DATABASE_HOSTNAME,
            self.DATABASE_PORT,
            self.DATABASE_NAME,
        )

        return f"{driver}://{user}:{password}@{host}:{port}/{name}"


database_settings = DatabaseSettings()


class CORSSettings(BaseSettings):
    ALLOW_ORIGINS: str
    ALLOW_CREDENTIALS: bool
    ALLOW_METHODS: str
    ALLOW_HEADERS: str


cors_settings = CORSSettings()


class AuthSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str


auth_settings = AuthSettings()


class BotSettings(BaseSettings):
    BOT_TOKEN: str


bot_settings = BotSettings()
