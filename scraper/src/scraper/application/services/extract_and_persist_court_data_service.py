from scraper.application.ports.extract_and_persist_court_data_use_case import (
    ExtractAndPersistCourtDataUseCase,
    ExtractAndPersistFilterRequest,
)
from scraper.domain.ports.court_case_extractor import (
    CourtCaseExtractor,
)
from scraper.domain.ports.court_case_repository import CourtCaseRepository


class ExtractAndPersistCourtDataService(ExtractAndPersistCourtDataUseCase):
    """
    Service to extract and persist court data.
    """

    def __init__(
        self,
        court_case_extractor: CourtCaseExtractor,
        court_case_repository: CourtCaseRepository,
    ) -> None:
        """
        Initializes the service with the necessary dependencies.

        :param court_case_extractor: An instance of CourtCaseExtractor to extract court data.
        :param court_case_repository: An instance of CourtCaseRepository to persist court data.
        """
        self.court_data_extractor = court_case_extractor
        self.court_case_repository = court_case_repository

    async def execute(self, filters: ExtractAndPersistFilterRequest) -> None:
        """
        Extracts court data for a given case ID and persists it.
        """
        court_cases = await self.court_data_extractor.extract(filters)
        print(f"Extracted {len(court_cases)} court cases.")

        for court_case in court_cases:
            await self.court_case_repository.save(court_case)
