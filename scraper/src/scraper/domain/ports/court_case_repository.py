"""Provides the abstract interface for case data storage and retrieval."""

from abc import ABC, abstractmethod

from scraper.domain.court_case import CourtCase


class CourtCaseRepository(ABC):
    """Abstract base class for a court case repository.

    This class defines the interface for a case repository, which is responsible for
    saving and retrieving cases. It is intended to be implemented by concrete classes
    that interact with a specific data storage solution (e.g., database, file system).
    """

    @abstractmethod
    def save(self, court_case: CourtCase) -> None:
        """Saves a case to the repository.

        :param case: The case to save.
        """
        pass
