from abc import ABC, abstractmethod

from scraper.domain.case import Case


class CaseRepository(ABC):
    @abstractmethod
    def save(self, case: Case) -> None:
        """
        Saves a case to the repository.
        
        :param case: The case to save.
        """
        pass
