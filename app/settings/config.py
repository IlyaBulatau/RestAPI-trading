from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
    env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="allow"
    )

    REDIS_HOST: str = "redis"


class DataBaseSettings(Settings):

    DB_LOGIN: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "postgres"
    DB_PORT: int = 5432
    DB_NAME: str = "postgres"

    def get_url(self) -> PostgresDsn:
        return f"postgresql+asyncpg://{self.DB_LOGIN}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class TokenSettings(Settings):

    TOKEN_ALGORITHM: str = "HS256"
    TOKEN_KEY: str = "1111"
    TOKEN_LIMIT_MINUTES: str = "10"
