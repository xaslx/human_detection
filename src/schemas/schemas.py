from pydantic import BaseModel


class PhotosOut(BaseModel):
    url: str