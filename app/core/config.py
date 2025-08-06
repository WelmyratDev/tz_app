from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "Task Management System App"
    DEBUG: bool = True
    DATABASE_URL: str
    SECRET_KEY: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str

    model_config = ConfigDict(
        env_file = ".env"
    )


@lru_cache
def get_settings():
    return Settings()

settings = get_settings()