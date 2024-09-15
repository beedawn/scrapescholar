# app/dependencies.py

from pydantic_settings import BaseSettings  # Updated import
from pydantic import Field

class Settings(BaseSettings):
    # Configuration for the PostgreSQL database connection
    POSTGRES_USER: str = "student"  # replace with your actual username
    POSTGRES_PASSWORD: str = "student"  # replace with your actual password
    POSTGRES_DB: str = "scrapescholartestdb"  # replace with your actual database name
    POSTGRES_SERVER: str = "localhost"  # replace with your actual server
    POSTGRES_PORT: str = "49168"  # replace with your actual port
    DATABASE_URL: str = Field(default="", description="The database URL")  # Initialize with an empty string

    # Generate DATABASE_URL dynamically if not provided
    @property
    def database_url(self) -> str:
        if not self.DATABASE_URL:
            # Construct the database URL dynamically
            return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        return self.DATABASE_URL

    class Config:
        env_file = ".env"  # This will load environment variables from a .env file if available

# Create a global settings object
settings = Settings()

def get_db_uri():
    """
    Generate the database URI dynamically based on environment variables or default settings.
    """
    return settings.database_url

# The `get_db` function that provides a SQLAlchemy database session
def get_db():
    from app.db.session import SessionLocal  # Import here to avoid circular import issues
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()