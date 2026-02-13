from pydantic import BaseModel


class MessageData(BaseModel):
    to: str
    topic: str
    message: str
