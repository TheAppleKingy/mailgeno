from pydantic_settings import BaseSettings


class Config(BaseSettings):
    mailgeno_sender: str
    mailgeno_password: str
    mailgeno_host: str
    mailgeno_port: int


conf = Config()  # type: ignore
