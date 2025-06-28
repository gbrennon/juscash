from abc import ABC, abstractmethod


class ExtractAndPersistCourtDataUseCase(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass
