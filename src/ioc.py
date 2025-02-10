from dishka import Provider, Scope, from_context, provide

from src.config import Config, load_settings
from src.repositories.base import BaseRepository
from src.repositories.sqlite import SqliteRepository
from src.services.human_detection import HumanDetection
from src.services.photos import BasePhotosService, PhotosService


class AppProvider(Provider):
    config: Config = from_context(provides=Config, scope=Scope.APP)
    settings: dict = load_settings(file_path='settings.json')


    @provide(scope=Scope.REQUEST)
    def get_sqlite_repository(self, config: Config) -> BaseRepository:
        return SqliteRepository(db_file=config.db_name)

    @provide(scope=Scope.REQUEST)
    def get_photos_service(self, repository: BaseRepository) -> BasePhotosService:
        return PhotosService(repository=repository)

    
    @provide(scope=Scope.APP)
    def human_detection_service(self) -> HumanDetection:
        return HumanDetection(
            x_min=self.settings['frame_area']['x_min'],
            y_min=self.settings['frame_area']['y_min'],
            x_max=self.settings['frame_area']['x_max'],
            y_max=self.settings['frame_area']['y_max'],
            photos_service=None,
        )