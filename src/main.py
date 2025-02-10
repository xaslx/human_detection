from contextlib import asynccontextmanager

from dishka import AsyncContainer, make_async_container
from dishka.integrations import fastapi as fastapi_integration
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.config import Config
from src.database.sqlite import init_db
from src.ioc import AppProvider
from src.routers.camera import router as camera_router
from src.routers.events import router as events_router
from src.routers.humans import router as humans_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    init_db()
    yield



def create_app() -> FastAPI:
    
    config: Config = Config()
    container: AsyncContainer = make_async_container(AppProvider(), context={Config: config})
    
    app: FastAPI = FastAPI(
        title='Human Detection',
        lifespan=lifespan,
        description='Приложение для определения человека в кадре и сохранения фотографии',
    )
    
    app.include_router(router=humans_router, prefix='/api/v1', tags=['Humans'])
    app.include_router(router=camera_router, prefix='/api/v1', tags=['Camera'])
    app.include_router(router=events_router, tags=['Events'])
    
    app.mount('/', StaticFiles(directory='src/static', html=True), name='static')

    
    fastapi_integration.setup_dishka(container=container, app=app)
    
    return app