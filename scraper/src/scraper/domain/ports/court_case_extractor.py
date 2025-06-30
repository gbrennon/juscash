"""Abstract base class for court scrapers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self

from scraper.domain.court_case import CourtCase

DATE_FMT = "%Y-%m-%d"


@dataclass(frozen=True)
class CourtCaseExtractorFilters:
    start_date: str | None = None
    end_date: str | None = None
    section_id: str | None = None
    search_terms: str | None = None

    @classmethod
    def from_raw(cls, raw_filters: dict[str, Any]) -> Self:
        """
        Create an instance from raw filter data.
        :param raw_filters: Dictionary containing filter parameters
        :return: CourtCaseExtractorFilters instance
        """

        def format_date(d: Any) -> str | None:
            if isinstance(d, datetime):
                return d.strftime(DATE_FMT)
            if isinstance(d, str):
                return d  # assume it's already correctly formatted
            return None

        return cls(
            start_date=format_date(raw_filters.get("start_date")),
            end_date=format_date(raw_filters.get("end_date")),
            section_id=raw_filters.get("section_id"),
            search_terms=raw_filters.get("search_terms"),
        )


class CourtCaseExtractor(ABC):
    """
    Abstract base class for court case extractors.
    This class defines the interface for extracting the Cases for a given Court.
    Subclasses should implement the `extract` method to define the specific extraction
    logic for different courts.
    """

    @abstractmethod
    def extract(self, filters: CourtCaseExtractorFilters) -> list[CourtCase]:
        """
        Extract case from the court.
        This method should be implemented by subclasses to define the extraction logic.
        """
        pass
