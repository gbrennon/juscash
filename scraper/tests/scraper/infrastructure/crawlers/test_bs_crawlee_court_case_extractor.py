from decimal import Decimal

import pytest

from scraper.domain.court_case import CourtCaseStatus
from scraper.domain.ports.court_case_extractor import CourtCaseExtractorFilters
from scraper.infrastructure.crawlers.bs_crawlee_court_case_extractor import (
    BsCrawleeCourtCaseExtractor,
)


@pytest.mark.integration
class TestBsCrawleeCourtCaseExtractor:
    """Integration tests using VCR to record/replay HTTP interactions"""

    @pytest.mark.asyncio
    @pytest.mark.vcr()
    async def test_extract_when_filters_provided_then_returns_court_cases(self):
        # Arrange
        search_terms = '"RPV"+e+"pagamento+pelo+INSS"'
        extractor = BsCrawleeCourtCaseExtractor()
        filters = CourtCaseExtractorFilters(
            start_date="01/06/2025",
            end_date="29/06/2025",
            section_id="123",
            search_terms=search_terms,
        )

        # Act
        result = await extractor.extract(filters)

        # Assert
        assert isinstance(result, list)
        assert len(result) > 0  # Assuming the recorded response has data

        for case in result:
            assert case.id is not None
            assert case.name is not None
            assert case.status == CourtCaseStatus.NEW
            assert case.amount.gross_principal == Decimal("1000.00")
            assert case.amount.interest == Decimal("1000.00")
            assert case.amount.lawyer_fees == Decimal("1000.00")
            assert isinstance(case.lawyers, list)

    @pytest.mark.asyncio
    @pytest.mark.vcr()
    async def test_extract_when_no_cases_found_then_returns_empty_list(self):
        # Arrange
        extractor = BsCrawleeCourtCaseExtractor()
        filters = CourtCaseExtractorFilters(
            start_date="01/01/2025",
            end_date="02/01/2025",  # Short date range likely to have no results
            search_terms="nonexistent_search_term_12345",
        )

        # Act
        result = await extractor.extract(filters)

        # Assert
        assert isinstance(result, list)
        assert len(result) == 0

    @pytest.mark.asyncio
    @pytest.mark.vcr()
    async def test_extract_when_no_filters_then_uses_defaults_and_returns_cases(self):
        # Arrange
        extractor = BsCrawleeCourtCaseExtractor()
        filters = CourtCaseExtractorFilters()  # All None

        # Act
        result = await extractor.extract(filters)

        # Assert
        assert isinstance(result, list)
        # The actual assertions depend on what your default behavior returns
