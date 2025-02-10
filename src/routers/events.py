import asyncio

from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse


router: APIRouter = APIRouter()


photo_events: list[str] = []


async def event_generator():
    while True:
        await asyncio.sleep(1)
        if photo_events:
            photo_url: str = photo_events.pop(0)
            yield photo_url


@router.get('/events')
async def events():
    return EventSourceResponse(event_generator())


def add_photo_event(photo_url: str):
    
    url: str = photo_url.replace('src/static', '')
    photo_events.append(url)
