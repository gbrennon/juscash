"""
Defines data models related to legal cases, including CourtCase and CourtCaseAmount.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum


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


class CourtCaseStatus(StrEnum):
    """Enumeration for court case statuses."""

    NEW = "new"
    READ = "read"
    PROCESSED = "processed"


@dataclass(frozen=True)
class CourtCase:
    """Represents a court case.

    This abstractiong encapsulates the essential details of a court case, including its
    unique identifier, name, status, and timestamps for creation and last update.
    """

    id: str  # Also known as case_id
    name: str
    lawyers: list[str]
    published_at: datetime
    status: CourtCaseStatus
    amount: CourtCaseAmount

    @property
    def case_id(self) -> str:
        """Alias for id."""
        return self.id
