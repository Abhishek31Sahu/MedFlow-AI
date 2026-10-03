from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # JWT
    SECRET_KEY: str = "change_this_to_a_long_random_secret_key"
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # OpenRouter
    OPENROUTER_API_KEY: str
    MODEL_NAME: str = "openai/gpt-4o-mini"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",   # Ignore any future extra env variables
    )


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()