from sqlalchemy.ext.asyncio import AsyncSession

from scraper.domain.court_case import CourtCase
from scraper.domain.ports.court_case_repository import CourtCaseRepository
from scraper.infrastructure.persistence.models.court_case_model import CourtCaseModel


class SQLAlchemyCourtCaseRepository(CourtCaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        """
        Initializes the repository with an SQLAlchemy session.

        :param session: An instance of AsyncSession for database operations.
        """
        self.session = session

    async def save(self, court_case: CourtCase) -> None:
        """
        Saves a court case to the database.
        :param court_case: The CourtCase instance to be saved.
        """
        model = CourtCaseModel.from_entity(court_case)
        print(f"Saving court case: {court_case.case_id} to the database...")

        async with self.session.begin():
            self.session.add(model)
            await self.session.commit()

            print(f"Saved court case: {court_case.case_id} to the database.")
