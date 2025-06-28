from decimal import Decimal

from scraper.domain.court_case import CourtCaseAmount


class TestCourtCaseAmount:
    def test_constructor_when_valid_then_succed(self):
        gross_principal = Decimal(1000)
        interest = Decimal(100)
        lawyer_fees = Decimal(50)

        amount = CourtCaseAmount(gross_principal, interest, lawyer_fees)

        assert isinstance(amount, CourtCaseAmount)
