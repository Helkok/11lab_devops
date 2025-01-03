from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str

    POSTGRES_URL: Optional[str] = None

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    ACCESS_TOKEN_EXPIRES_MIN: int

    class Config:
        env_file = '.env'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.POSTGRES_URL = f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
