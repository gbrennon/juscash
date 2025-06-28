from dataclasses import dataclass

@dataclass(frozen=True)
class CaseAmount:
    """
    Represents an amount of money.
    """
    gross_principal: float
    interest: float
    lawyer_fees: float

    @property
    def total(self) -> float:
        """
        Returns the total amount, which is the sum of gross principal, interest, and lawyer fees.
        """
        return self.gross_principal + self.interest + self.lawyer_fees

@dataclass(frozen=True)
class Case:
    """
    This can also be called a CourtCase, CivilCase and CriminalCase...
    """
    id: str # Also known as case_id
    name: str
    status: str
    created_at: str
    updated_at: str
