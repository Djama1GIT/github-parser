from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    class Config:
        env_file = '.env'

    NAME: str = os.getenv("NAME")

    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT: int = os.getenv("POSTGRES_PORT")

    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: int = os.getenv("REDIS_PORT")

    @property
    def DATABASE_URL(self) -> str:
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}' \
               f'@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
