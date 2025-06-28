from dataclasses import dataclass

class AggregateRoot:
    def __init__(self, id: str):
        self._id = id
        
    @abstractproperty
    def id(self) -> str:
        pass

@dataclass(frozen=True)
class Case(AggregateRoot):
    """
    This can also be called a CourtCase, CivilCase and CriminalCase...
    """
    case_id: str
    name: str
    court_id: str
    case_number: str
    status: str
    date_filed: str
    date_last_modified: str

    @property
    def id(self) -> str:
        return self.case_id
