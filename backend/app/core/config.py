import os

from dotenv import load_dotenv
from pydantic import ConfigDict
from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Blog Managing API"
    PROJECT_VERSION: str = "0.1.0"
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    AI_API_KEY: str = os.getenv("AI_API_KEY")
    REDIS_URL: str = os.getenv("REDIS_URL")
    AI_USER_PASSWORD: str = os.getenv("AI_USER_PASSWORD")

    model_config = ConfigDict(env_file="backend/app/.env", case_sensitive=True)


settings = Settings()
