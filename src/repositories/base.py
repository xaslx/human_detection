from abc import ABC, abstractmethod
from datetime import date


class BaseRepository(ABC):
    
    @abstractmethod
    def save(self, obj: object) -> None:
        pass

    @abstractmethod
    def get(self, obj_id: int) -> dict | None:
        pass

    @abstractmethod
    def get_all(self) -> list[dict] | None:
        pass

    @abstractmethod
    def get_by_date(self, start_date: date, end_date: date) -> list[dict] | None:
        ...