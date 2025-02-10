from typing import Annotated

from dishka.integrations.fastapi import FromDishka as Depends
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Query, status

from src.schemas.filters import DateFilter
from src.schemas.schemas import PhotosOut
from src.services.photos import BasePhotosService


router: APIRouter = APIRouter()


@router.get(
    '/humans',
    status_code=status.HTTP_200_OK,
    description='Эндпоинт для получения списка ссылок фотографий по датам',
)
@inject
async def get_list_photo_handler(
    photos_service: Depends[BasePhotosService],
    filter: Annotated[DateFilter, Query()],
) -> list[PhotosOut] | None:
    
    photos: list[dict] | None = photos_service.get_photos_by_date(
        start_date=filter.start_date, 
        end_date=filter.end_date
    )
    photos = [photo.get('filename') for photo in photos]
    return [PhotosOut(url=url) for url in photos]
    