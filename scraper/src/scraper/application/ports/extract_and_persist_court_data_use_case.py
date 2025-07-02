from abc import ABC, abstractmethod

from scraper.domain.ports.court_case_extractor import CourtCaseExtractorFilters

ExtractAndPersistFilterRequest = CourtCaseExtractorFilters


class ExtractAndPersistCourtDataUseCase(ABC):
    @abstractmethod
    async def execute(self, filters: ExtractAndPersistFilterRequest) -> None:
        pass
