"""Abstract base class for court scrapers."""

from abc import ABC, abstractmethod

from scraper.domain.court_case import CourtCase


class CourtCaseExtractor(ABC):
    """
    Abstract base class for court case extractors.
    This class defines the interface for extracting the Cases for a given Court.
    Subclasses should implement the `extract` method to define the specific extraction
    logic for different courts.
    """

    @abstractmethod
    def extract(self) -> list[CourtCase]:
        """
        Extract case from the court.
        This method should be implemented by subclasses to define the extraction logic.
        """
        pass
