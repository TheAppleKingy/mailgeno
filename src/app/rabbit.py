import json

from aio_pika import connect_robust
from aio_pika.abc import AbstractRobustChannel, AbstractRobustConnection, AbstractRobustQueue, AbstractIncomingMessage

from src.app.base import AbstractEmailSenderApp
from src.app.loop_lock import LoopLockMixin
from src.logger import logger


class RabbitEmailSenderApp(AbstractEmailSenderApp, LoopLockMixin):
    def __init__(self, conn_url: str, listen_for: str):
        super().__init__(conn_url, listen_for)
        self._connection: AbstractRobustConnection = None  # type: ignore
        self._channel: AbstractRobustChannel = None  # type: ignore
        self._queue: AbstractRobustQueue = None  # type: ignore

    async def validate_data(self, data: AbstractIncomingMessage) -> dict[str, str]:
        return json.loads(data.body.decode())

    def return_func(self, ok: bool): return None

    async def run(self):
        self._connection = await connect_robust(self._conn_url)
        self._channel = await self._connection.channel()
        self._queue = await self._channel.declare_queue(self._listen_for, durable=False)
        await self._queue.consume(self.on_event(), no_ack=True)
        logger.info(f"RabbitEmailSenderApp started. Ready to accept tasks")
        await self.keep()
