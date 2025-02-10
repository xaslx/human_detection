import threading

from dishka.integrations.fastapi import FromDishka as Depends
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.services.human_detection import HumanDetection
from src.services.photos import BasePhotosService


router: APIRouter = APIRouter()


@router.post(
    '/start',
    status_code=status.HTTP_200_OK,
    description='Эндпоинт для включения камеры',
)
@inject
async def start_camera_handler(
    human_detection: Depends[HumanDetection], 
    photos_service: Depends[BasePhotosService]
) -> JSONResponse:
    
    if not human_detection.is_running:
        human_detection.photos_service = photos_service
        thread = threading.Thread(target=human_detection.start, daemon=True)
        thread.start()
        return JSONResponse(content={'detail': 'Камера запущена'})
    
    return JSONResponse(content={'detail': 'Камера уже запущена'})


@router.post(
    '/stop',
    status_code=status.HTTP_200_OK,
    description='Эндпоинт для выключения камеры',
)
@inject
async def stop_camera_handler(human_detection: Depends[HumanDetection]) -> JSONResponse:
    
    if human_detection.is_running:
        human_detection.stop()
        return JSONResponse(content={'detail': 'Камера остановлена'})
    
    return JSONResponse(content={'detail': 'Камера уже остановлена'})