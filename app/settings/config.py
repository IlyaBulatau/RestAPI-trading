from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, EmailStr


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="allow"
    )

    APP_HOST: str = "localhost"
    APP_PORT: int = 5555

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379


class DataBaseSettings(Settings):
    DB_LOGIN: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "postgres"
    DB_PORT: int = 5432
    DB_NAME: str = "postgres"
    DB_ECHO: bool = True

    def get_url(self) -> PostgresDsn:
        return f"postgresql+asyncpg://{self.DB_LOGIN}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class TokenSettings(Settings):
    TOKEN_ALGORITHM: str = "HS256"
    TOKEN_KEY: str = "1111"
    TOKEN_LIMIT_MINUTES: str = "10"


class SMTPSettings(Settings):
    LOGGER_EMAIL: EmailStr | None = None
    LOGGER_PASSWORD: str | None = None
    LOGGER_HOST: str | None = None
    LOGGER_PORT: int | None = None
    LOGGER_SUBJECT: str = "FastAPI server"
