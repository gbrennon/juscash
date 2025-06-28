"""Abstract base class for court scrapers."""

from abc import ABC, abstractmethod

from scraper.domain.case import Case


class CourtCaseExtractor(ABC):
    """
    Abstract base class for court case extractors.
    This class defines the interface for extracting the Cases for a given Court.
    Subclasses should implement the `extract` method to define the specific extraction
    logic for different courts.
    """

    @abstractmethod
    def extract(self) -> list[Case]:
        """
        Extract case from the court.
        This method should be implemented by subclasses to define the extraction logic.
        """
        pass
