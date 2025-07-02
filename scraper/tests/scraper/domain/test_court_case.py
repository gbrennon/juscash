from datetime import datetime
from decimal import Decimal

import pytest

from scraper.domain.court_case import CourtCase, CourtCaseAmount, CourtCaseStatus


class TestCourtCaseAmount:
    def test_constructor_when_valid_then_succed(self):
        gross_principal = Decimal(1000)
        interest = Decimal(100)
        lawyer_fees = Decimal(50)

        amount = CourtCaseAmount(gross_principal, interest, lawyer_fees)

        assert isinstance(amount, CourtCaseAmount)

    def test_constructor_when_gross_principal_is_none_then_raise_value_error(self):
        gross_principal = None
        interest = Decimal(100)
        lawyer_fees = Decimal(50)

        with pytest.raises(ValueError, match="gross_principal cannot be None") as _:
            CourtCaseAmount(gross_principal, interest, lawyer_fees)

    def test_constructor_when_interest_is_none_then_raise_value_error(self):
        gross_principal = Decimal(1000)
        interest = None
        lawyer_fees = Decimal(50)

        with pytest.raises(ValueError, match="interest cannot be None") as _:
            CourtCaseAmount(gross_principal, interest, lawyer_fees)

    def test_constructor_when_lawyer_fees_is_none_then_raise_value_error(self):
        gross_principal = Decimal(1000)
        interest = Decimal(100)
        lawyer_fees = None

        with pytest.raises(ValueError, match="lawyer_fees cannot be None") as _:
            CourtCaseAmount(gross_principal, interest, lawyer_fees)

    def test_total_when_all_fields_are_set_then_return_correct_total(self):
        gross_principal = Decimal(1000)
        interest = Decimal(100)
        lawyer_fees = Decimal(50)

        amount = CourtCaseAmount(gross_principal, interest, lawyer_fees)

        expected_total = Decimal(1000 + 100 + 50)
        assert amount.total == expected_total

    def test_total_when_any_field_is_zero_then_return_correct_total(self):
        gross_principal = Decimal(0)
        interest = Decimal(100)
        lawyer_fees = Decimal(50)

        amount = CourtCaseAmount(gross_principal, interest, lawyer_fees)

        expected_total = Decimal(0 + 100 + 50)
        assert amount.total == expected_total

    def test_total_when_all_fields_are_zero_then_return_zero(self):
        gross_principal = Decimal(0)
        interest = Decimal(0)
        lawyer_fees = Decimal(0)

        amount = CourtCaseAmount(gross_principal, interest, lawyer_fees)

        expected_total = Decimal(0 + 0 + 0)
        assert amount.total == expected_total

class TestCourtCase:
    def test_case_id_when_called_then_return_id(self):
        gross_principal = Decimal(1000)
        interest = Decimal(100)
        lawyer_fees = Decimal(50)
        amount = CourtCaseAmount(gross_principal, interest, lawyer_fees)
        court_case_id = "case-123"

        case = CourtCase(
            id=court_case_id,
            name="Test Case",
            lawyers=["Lawyer A", "Lawyer B"],
            published_at=datetime.now(),
            status=CourtCaseStatus.NEW,
            amount=amount
        )

        expected_case_id = court_case_id
        assert case.case_id == expected_case_id
        assert case.id == expected_case_id
