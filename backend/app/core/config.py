import os
from pydantic.v1 import BaseSettings

from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Blog Managing API"
    PROJECT_VERSION: str = "0.1.0"
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    JWT_SECRET: str = os.getenv("JWT_SECRET")

    class Config:
        env_file = "backend/app/.env"
        case_sensitive = True


settings = Settings()
