from unittest import mock

import pytest

from scraper.application.ports.extract_and_persist_court_data_use_case import (
    ExtractAndPersistFilterRequest,
)
from scraper.application.services.extract_and_persist_court_data_service import (
    ExtractAndPersistCourtDataService,
)
from scraper.domain.court_case import CourtCase
from scraper.domain.ports.court_case_extractor import CourtCaseExtractor
from scraper.domain.ports.court_case_repository import CourtCaseRepository


@pytest.fixture()
def filters() -> ExtractAndPersistFilterRequest:
    """Fixture to provide default filters for the extractor.
    # This fixture can be used to set up common mocks or configurations if needed
    """
    return ExtractAndPersistFilterRequest(
        start_date="01-10-2024",
        end_date="01-13io2024",
        section_id="13",
        search_terms='"RPV"+e+"pagamento+pelo+INSS"',
    )


class TestExtractAndPersistCourtDataService:
    @pytest.mark.asyncio
    async def test_execute_when_extract_returns_cases_then_calls_save_for_each_case(
        self,
        filters: ExtractAndPersistFilterRequest,
    ) -> None:
        # Arrange
        mock_court_case_extractor = mock.AsyncMock(spec=CourtCaseExtractor)
        mock_court_case_repository = mock.AsyncMock(spec=CourtCaseRepository)
        mock_cases = [
            mock.AsyncMock(spec=CourtCase),
            mock.AsyncMock(spec=CourtCase),
        ]
        mock_court_case_extractor.extract.return_value = mock_cases
        service = ExtractAndPersistCourtDataService(
            court_case_extractor=mock_court_case_extractor,
            court_case_repository=mock_court_case_repository,
        )

        # Act
        await service.execute(filters)

        # Assert
        expected_call_args = [
            mock.call(mock_cases[0]),
            mock.call(mock_cases[1]),
        ]
        mock_court_case_repository.save.assert_has_calls(expected_call_args)

    @pytest.mark.asyncio
    async def test_execute_when_extractor_raises_exception_then_let_it_raise(
        self,
        filters: ExtractAndPersistFilterRequest,
    ) -> None:
        # Arrange
        mock_court_case_extractor = mock.AsyncMock(spec=CourtCaseExtractor)
        mock_court_case_repository = mock.AsyncMock(spec=CourtCaseRepository)
        mock_court_case_extractor.extract.side_effect = Exception("Extraction failed")
        service = ExtractAndPersistCourtDataService(
            court_case_extractor=mock_court_case_extractor,
            court_case_repository=mock_court_case_repository,
        )

        # Act & Assert
        with pytest.raises(Exception) as _:
            await service.execute(filters)

    @pytest.mark.asyncio
    async def test_execute_when_repository_raises_exception_then_let_it_raise(
        self,
        filters: ExtractAndPersistFilterRequest,
    ) -> None:
        # Arrange
        mock_court_case_extractor = mock.AsyncMock(spec=CourtCaseExtractor)
        mock_court_case_repository = mock.AsyncMock(spec=CourtCaseRepository)
        mock_cases = [
            mock.AsyncMock(spec=CourtCase),
            mock.AsyncMock(spec=CourtCase),
        ]
        mock_court_case_extractor.extract.return_value = mock_cases
        mock_court_case_repository.save.side_effect = Exception("Save failed")
        service = ExtractAndPersistCourtDataService(
            court_case_extractor=mock_court_case_extractor,
            court_case_repository=mock_court_case_repository,
        )

        # Act & Assert
        with pytest.raises(Exception) as _:
            await service.execute(filters)
