from abc import ABC, abstractmethod


class ExtractAndPersistCourtDataUseCase(ABC):
    @abstractmethod
    async def execute(self) -> None:
        pass
