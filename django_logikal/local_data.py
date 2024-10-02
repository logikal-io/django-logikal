from abc import ABC, abstractmethod


class SkipInsert(Exception):
    """
    Exception class for skipping an insertion.
    """


class LocalData(ABC):
    """
    Base class for local data insertion.
    """
    @staticmethod
    @abstractmethod
    def insert() -> None:
        ...
