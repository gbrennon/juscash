from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from scraper.application.services.extract_and_persist_court_data_service import (
    ExtractAndPersistCourtDataService,
)
from scraper.infrastructure.crawlers.bs_crawlee_court_case_extractor import (
    BsCrawleeCourtCaseExtractor,
)
from scraper.infrastructure.database_config import DatabaseConfig
from scraper.infrastructure.persistence.repositories import SQLAlchemyCourtCaseRepository

database_config = DatabaseConfig.from_env()

# Singleton engine
engine = create_async_engine(database_config.url, echo=True)

# Singleton sessionmaker
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


def get_extract_and_persist_course_case_service(
    session: AsyncSession,
) -> ExtractAndPersistCourtDataService:
    court_case_extractor = BsCrawleeCourtCaseExtractor()
    court_case_repository = SQLAlchemyCourtCaseRepository(session)

    return ExtractAndPersistCourtDataService(
        court_case_extractor=court_case_extractor, court_case_repository=court_case_repository
    )
