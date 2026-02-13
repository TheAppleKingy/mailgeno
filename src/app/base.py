from abc import ABC, abstractmethod
from typing import TypeVar, Any, Awaitable, Callable, overload

from src.dto import MessageData
from src.sender import send_mail
from src.logger import logger

IncomingData = TypeVar("IncomingData", bound=Any)
HandlerType = Callable[[IncomingData], Awaitable[Any]]


class AbstractEmailSenderApp(ABC):
    def __init__(self, conn_url: str, listen_for: str):
        self._conn_url = conn_url
        self._listen_for = listen_for

    @abstractmethod
    async def validate_data(self, data: IncomingData) -> dict[str, str]: ...

    @abstractmethod
    async def return_func(self, ok: bool) -> Any: ...

    def on_event(self) -> HandlerType:
        async def handler(incoming_data: IncomingData):
            ok = True
            try:
                model = MessageData.model_validate(await self.validate_data(incoming_data))
                send_mail(model.to, model.topic, model.message)
            except Exception as e:
                ok = False
                logger.error(f"Error occured: {e}")
            return self.return_func(ok)
        return handler

    @abstractmethod
    async def run(self): ...
