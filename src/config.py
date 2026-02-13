from pydantic_settings import BaseSettings


class Config(BaseSettings):
    sender: str
    password: str
    host: str
    port: str


conf = Config()
