import pytest

from scraper.infrastructure.container import (
    get_db_session,
    get_extract_and_persist_course_case_service,
)


@pytest.mark.integration
class TestContainer:
    @pytest.mark.asyncio
    async def test_get_session(self) -> None:
        async with get_db_session() as session:
            assert session is not None
            assert hasattr(session, "execute")

    @pytest.mark.asyncio
    async def test_get_extract_and_persist_course_case_service(self) -> None:
        async with get_db_session() as session:
            service = get_extract_and_persist_course_case_service(session)
            assert service is not None
            assert hasattr(service, "execute")
