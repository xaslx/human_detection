from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date, datetime

from src.repositories.base import BaseRepository


@dataclass
class BasePhotosService(ABC):
    repository: BaseRepository
    
    @abstractmethod
    def save_photo(self, filename: str, timestamp: datetime) -> None:
        ...

    @abstractmethod
    def get_all_photos(self) -> list[dict] | None:
        ...

    @abstractmethod
    def get_photos_by_date(self, start_date: date, end_date: date) -> list[dict] | None:
        ...


@dataclass
class PhotosService(BasePhotosService):
    

    def save_photo(self, filename: str, timestamp: datetime) -> None:

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        photo_data = {'filename': filename, 'timestamp': timestamp}
        self.repository.save(photo_data)

    def get_all_photos(self) -> list[dict] | None:
        return self.repository.get_all()

    def get_photos_by_date(self, start_date: date, end_date: date) -> list[dict] | None:
        return self.repository.get_by_date(start_date, end_date)