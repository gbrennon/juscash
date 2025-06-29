"""
Defines data models related to legal cases, including CourtCase and CourtCaseAmount.
"""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class CourtCaseAmount:
    gross_principal: Decimal
    interest: Decimal
    lawyer_fees: Decimal

    def __post_init__(self):
        """Validate that no field is None."""
        for field_name, value in [
            ("gross_principal", self.gross_principal),
            ("interest", self.interest),
            ("lawyer_fees", self.lawyer_fees),
        ]:
            if value is None:
                raise ValueError(f"{field_name} cannot be None")

    @property
    def total(self) -> Decimal:
        return self.gross_principal + self.interest + self.lawyer_fees


@dataclass(frozen=True)
class CourtCase:
    """Represents a court case.

    This abstractiong encapsulates the essential details of a court case, including its
    unique identifier, name, status, and timestamps for creation and last update.
    """

    id: str  # Also known as case_id
    name: str
    status: str
    defendant: str
    amount: CourtCaseAmount
    published_at: date
