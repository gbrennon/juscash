import os
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    """Database configuration for PostgreSQL."""

    url: str
    echo: bool = False
    pool_size: int = 10
    max_overflow: int = 20
    pool_pre_ping: bool = True
    pool_recycle: int = 3600

    @classmethod
    def from_env(cls) -> "DatabaseConfig":
        """Create database config from environment variables."""
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "5432")
        name = os.getenv("DB_NAME", "scraper_db")
        user = os.getenv("DB_USER", "scraper_user")
        password = os.getenv("DB_PASSWORD", "password")

        # Allow full DATABASE_URL override
        database_url = os.getenv(
            "DATABASE_URL",
            f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}",
        )

        return cls(
            url=database_url,
            echo=os.getenv("DB_ECHO", "false").lower() == "true",
            pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
            max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "20")),
            pool_recycle=int(os.getenv("DB_POOL_RECYCLE", "3600")),
        )
