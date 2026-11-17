from abc import ABC, abstractmethod


class DocumentReader(ABC):

    @abstractmethod
    def supports(self, file_type: str) -> bool:
        ...

    @abstractmethod
    def read(self, file_path: str) -> str:
        ...