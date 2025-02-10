import json

from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    db_name: str = Field(alias='DB_NAME')
    
    
def load_settings(file_path: str):
    with open(file_path, 'r') as file:
        settings_data = file.read()
        settings = json.loads(settings_data)
    return settings