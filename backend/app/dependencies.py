# app/dependencies.py

from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv
import os


load_dotenv()


class Settings(BaseSettings):
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")  # Loaded from .env
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")  # Loaded from .env
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")  # Loaded from .env
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")  # Loaded from .env
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")  # Loaded from .env
    DATABASE_URL: str = Field(default="", description="The database URL")  # Initialize with an empty string

    # Generate DATABASE_URL dynamically if not provided
    @property
    def database_url(self) -> str:
        if not self.DATABASE_URL:
            # Construct the database URL dynamically
            return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        return self.DATABASE_URL


# Create a global settings object
settings = Settings()


def get_db_uri():
    """
    Generate the database URI dynamically based on environment variables or default settings.
    """
    return settings.database_url


def get_db():
    from app.db.session import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
