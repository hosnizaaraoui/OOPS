from abc import ABC, abstractmethod


class Host(ABC):

    @abstractmethod
    def execute(self, command: list[str]) -> str:
        pass
