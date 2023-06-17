from abc import ABC, abstractmethod


class LocalData(ABC):
    """
    Base class for local data insertion.
    """
    @staticmethod
    @abstractmethod
    def insert() -> None:
        ...
