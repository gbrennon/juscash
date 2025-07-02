from dataclasses import dataclass


@dataclass(frozen=True)
class CourtCaseDetailsRequest:
    """
    Represents a request for court case details.
    """

    case_id: str

    def __str__(self):
        return f"CourtCaseDetailsRequest(case_id={self.case_id})"
