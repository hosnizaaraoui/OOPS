from abc import ABC, abstractmethod


class Host(ABC):

    @abstractmethod
    async def execute(self, command: list[str]) -> str:
        pass
