from datetime import UTC, datetime
from decimal import Decimal

from scraper.domain.court_case import CourtCase, CourtCaseAmount, CourtCaseStatus
from scraper.infrastructure.persistence.models.court_case_model import CourtCaseModel


class TestCourtCaseModel:
    def test_to_entity_when_all_fields_are_set_then_return_correct_entity(self):
        # Arrange
        case_number = "12345"
        name = "Fake Court Case"
        lawyers = ["Lawyer A", "Lawyer B"]
        gross_principal = Decimal(1000)
        interest = Decimal(100)
        lawyer_fees = Decimal(50)
        published_at = datetime.now(UTC)

        court_case = CourtCaseModel(
            id=case_number,
            name=name,
            lawyers=lawyers,
            published_at=published_at,
            status=CourtCaseStatus.NEW,
            gross_principal=gross_principal,
            interest=interest,
            lawyer_fees=lawyer_fees,
        )

        # Act
        entity = court_case.to_entity()

        # Assert
        expected_court_case_amount = CourtCaseAmount(
            gross_principal=gross_principal, interest=interest, lawyer_fees=lawyer_fees
        )
        assert entity.id == case_number
        assert entity.name == name
        assert entity.lawyers == lawyers
        assert entity.published_at == published_at
        assert entity.status == CourtCaseStatus.NEW
        assert isinstance(entity.amount, CourtCaseAmount)
        assert entity.amount == expected_court_case_amount
        assert entity.amount.total == Decimal(1150)

    def test_from_entity_when_fields_are_set_then_return_correct_model(self):
        # Arrange
        case_number = "12345"
        name = "Fake Court Case"
        lawyers = ["Lawyer A", "Lawyer B"]
        amount = CourtCaseAmount(Decimal(1000), Decimal(100), Decimal(50))
        published_at = datetime.now(UTC)

        entity = CourtCase(
            id=case_number,
            name=name,
            lawyers=lawyers,
            amount=amount,
            published_at=published_at,
            status=CourtCaseStatus.NEW,
            content="This is a test case content.",
        )

        # Act
        model = CourtCaseModel.from_entity(entity)

        # Assert
        expected_gross_principal_value = 1000
        expected_interest_value = 100
        expected_lawyer_fees_value = 50
        expected_content_value = "This is a test case content."
        assert model.id == case_number
        assert model.name == name
        assert model.gross_principal == expected_gross_principal_value
        assert model.interest == expected_interest_value
        assert model.lawyer_fees == expected_lawyer_fees_value
        assert model.content == expected_content_value
