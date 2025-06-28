"""
Defines data models related to legal cases, including CourtCase and CourtCaseAmount.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CourtCaseAmount:
    """Represents an amount of money related to a court case.

    This class encapsulates the financial details of a court case, including the gross
    principal, interest and lawyer fees. It provides a property to calculate the total
    amount by summing these components.

    Attributes:
        gross_principal (float): The principal amount before any deductions.
        interest (float): The interest amount applied to the principal.
        lawyer_fees (float): The fees charged by the lawyer for handling the case.
    """

    gross_principal: float
    interest: float
    lawyer_fees: float

    @property
    def total(self) -> float:
        """Returns the total amount.

        This property calculates the total amount by summing the gross principal,
        interest, and lawyer fees.
        """
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
    amount: CourtCaseAmount
    created_at: str
    updated_at: str
