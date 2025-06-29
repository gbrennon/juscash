from decimal import Decimal

import pytest

from scraper.domain.court_case import CourtCaseAmount


class TestCourtCaseAmount:
    def test_constructor_when_valid_then_succed(self):
        gross_principal = Decimal(1000)
        interest = Decimal(100)
        lawyer_fees = Decimal(50)

        amount = CourtCaseAmount(gross_principal, interest, lawyer_fees)

        assert isinstance(amount, CourtCaseAmount)

    def test_constructor_when_gross_principal_is_none_then_raise_value_error(self):
        # gross_principal = Decimal(1000)
        # interest = Decimal(100)
        # lawyer_fees = Decimal(50)
        gross_principal = None
        interest = Decimal(100)
        lawyer_fees = Decimal(50)

        with pytest.raises(ValueError, match="gross_principal cannot be None") as _:
            CourtCaseAmount(gross_principal, interest, lawyer_fees)

    def test_constructor_when_interest_is_none_then_raise_value_error(self):
        # gross_principal = Decimal(1000)
        # interest = Decimal(100)
        # lawyer_fees = Decimal(50)
        gross_principal = Decimal(1000)
        interest = None
        lawyer_fees = Decimal(50)

        with pytest.raises(ValueError, match="interest cannot be None") as _:
            CourtCaseAmount(gross_principal, interest, lawyer_fees)

    def test_constructor_when_lawyer_fees_is_none_then_raise_value_error(self):
        # gross_principal = Decimal(1000)
        # interest = Decimal(100)
        # lawyer_fees = Decimal(50)
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
