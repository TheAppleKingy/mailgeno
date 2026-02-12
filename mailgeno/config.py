from typing import Optional

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    sender: str
    password: str
    host: str
    port: str
    broker_url: Optional[str] = None
    resource: Optional[str] = None


conf = Config()
