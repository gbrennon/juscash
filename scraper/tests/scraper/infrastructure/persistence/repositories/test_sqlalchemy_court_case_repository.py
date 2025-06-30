import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from scraper.infrastructure.persistence.models.court_case_model import CourtCaseModel
from scraper.infrastructure.persistence.repositories import (
    SQLAlchemyCourtCaseRepository
)
from scraper.domain.court_case import CourtCase, CourtCaseAmount, CourtCaseStatus
from datetime import datetime
from decimal import Decimal

class TestSQLAlchemyCourtCaseRepository:
    @pytest.mark.asyncio
    async def test_save_when_called_then_persists_model(self, async_session: AsyncSession):
        # Arrange
        actual_id = "uuid-12345"
        court_case = CourtCase(
            id=actual_id,
            name="Test Case",
            lawyers=[],
            status=CourtCaseStatus.NEW,
            amount=CourtCaseAmount(
                gross_principal=Decimal('1000.00'),
                interest=Decimal('500.00'),
                lawyer_fees=Decimal('500.00')
            ),
            published_at=datetime.now()
        )
        repository = SQLAlchemyCourtCaseRepository(async_session)

        # Act
        await repository.save(court_case)

        # Assert
        persisted_case = await async_session.get(CourtCaseModel, actual_id)
        assert persisted_case is not None
        assert persisted_case.id == actual_id
        assert persisted_case.name == "Test Case"
        assert persisted_case.status == CourtCaseStatus.NEW
        assert persisted_case.gross_principal == Decimal('1000.00')
        assert persisted_case.interest == Decimal('500.00')
        assert persisted_case.lawyer_fees == Decimal('500.00')
        assert persisted_case.published_at is not None
        assert persisted_case.lawyers == []
