

from typing import Any
from scraper.domain.ports.court_case_extractor import CourtCaseExtractorFilters


class TestCourtCaseExtractorFilters:
    def test_from_raw_when_all_fields_present_then_create_instance_based_on_them(
        self
    ) -> None:
        # Arrange
        raw_filters: dict[str, str] = {
            "start_date": "2023-01-01",
            "end_date": "2023-12-31",
            "section_id": "123",
            "search_terms": "test"
        }

        # Act
        filters = CourtCaseExtractorFilters.from_raw(raw_filters)

        # Assert
        assert filters.start_date == "2023-01-01"
        assert filters.end_date == "2023-12-31"
        assert filters.section_id == "123"
        assert filters.search_terms == "test"

    def test_constructor_when_no_fields_then_create_instance_with_none(self) -> None:
        # Arrange
        raw_filters: dict[str, str] = {
        }

        # Act
        filters = CourtCaseExtractorFilters.from_raw(raw_filters)

        # Assert
        assert filters.start_date is None
        assert filters.end_date is None
        assert filters.section_id is None
        assert filters.search_terms is None

    def test_constructor_when_start_date_none_then_create_instance_with_none(
        self
    ) -> None:
        # Arrange
        raw_filters: dict[str, Any] = {
            "start_date": None,
            "end_date": "2023-12-31",
            "section_id": "123",
            "search_terms": "test"
        }

        # Act
        filters = CourtCaseExtractorFilters.from_raw(raw_filters)

        # Assert
        assert filters.start_date is None
        assert filters.end_date is "2023-12-31"
        assert filters.section_id is "123"
        assert filters.search_terms is "test"
