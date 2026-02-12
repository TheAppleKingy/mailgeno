from abc import ABC, abstractmethod

from mailgeno.abc import SenderType


class AbstractEmailSenderApp(ABC):
    def __init__(self, conn_url: str):
        self._conn_url = conn_url
        self._sender_func: SenderType = None

    def add_handler(self, sender: SenderType):
        if not self._sender_func:
            self._sender_func = sender

    @abstractmethod
    async def run(self): ...
