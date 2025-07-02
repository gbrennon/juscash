# scraper/src/scraper/infrastructure/persistence/migrations/env.py

# Standard library imports
import asyncio
import sys
from logging.config import fileConfig
from pathlib import Path

# Third-party imports
from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

# Local application imports (THESE MUST BE HERE)
from scraper.infrastructure.database_config import DatabaseConfig
from scraper.infrastructure.persistence.models.base import Base

# --- START OF CRITICAL PATH ADJUSTMENT (This block comes AFTER all imports) ---

# Get the absolute path to the directory containing env.py
current_dir = Path(__file__).resolve().parent

# The 'src' directory of your main 'scraper' Python package is 3 levels up:
# current_dir (migrations) -> persistence -> infrastructure -> scraper (your python package root)
# So, three .parent calls from current_dir leads to the 'scraper' python package.
# Example path in container: /app/scraper/src/scraper
scraper_package_root = current_dir.parent.parent.parent

# Now, the directory that *contains* this 'scraper' package is 'src'.
# This is the path we need to add to sys.path.
# Example path in container: /app/scraper/src
project_src_root = scraper_package_root.parent

# Add this 'src' directory to Python's system path
sys.path.insert(0, str(project_src_root))

# --- END OF CRITICAL PATH ADJUSTMENT ---


# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the target metadata for autogenerate support
target_metadata = Base.metadata

# Get database URL from your config
# Ensure DatabaseConfig correctly reads environment variables or alembic.ini
db_config = DatabaseConfig.from_env()


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = db_config.url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Create an Engine and associate a connection with the context."""
    connectable = create_async_engine(
        db_config.url,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
