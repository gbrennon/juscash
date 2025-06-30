from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
import vcr
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool

# Import your models
from scraper.infrastructure.persistence.models.base import Base

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="session")
async def engine() -> AsyncGenerator[AsyncEngine, None]:
    """Create engine and setup database."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def async_session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """🪄 Automagic database: creates, migrates, provides session, resets after test."""
    connection = await engine.connect()
    transaction = await connection.begin()

    session_factory = async_sessionmaker(
        bind=connection,
        class_=AsyncSession,
        expire_on_commit=False,
        future=True,
    )
    session = session_factory()

    try:
        yield session
    finally:
        await session.close()
        await transaction.rollback()  # Auto-reset database
        await connection.close()


@pytest.fixture(scope="session")
def event_loop():
    import asyncio

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# Configure VCR for async HTTP libraries
vcr_config = vcr.VCR(
    serializer="yaml",
    cassette_library_dir="tests/fixtures/vcr_cassettes",
    record_mode="once",  # Record once, then replay
    match_on=["uri", "method"],
    filter_headers=["authorization", "user-agent"],  # Don't record sensitive headers
    decode_compressed_response=True,
)


@pytest.fixture
def vcr_cassette():
    """Fixture to provide VCR cassette functionality"""
    return vcr_config
