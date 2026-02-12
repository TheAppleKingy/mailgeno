import json

from aio_pika import connect_robust
from aio_pika.abc import AbstractRobustChannel, AbstractRobustConnection, AbstractRobustQueue, AbstractIncomingMessage
from mailgeno.dto import MessageData

from mailgeno.logger import logger
from .base import AbstractEmailSenderApp
from .loop_lock import LoopLockMixin


class RabbitApp(AbstractEmailSenderApp, LoopLockMixin):
    def __init__(
        self,
        conn_url: str,
        queue_name: str
    ):
        super().__init__(conn_url)
        self._connection: AbstractRobustConnection = None
        self._channel: AbstractRobustChannel = None
        self._queue_name = queue_name
        self._queue: AbstractRobustQueue = None

    async def _handle_validated(self):
        pass

    def _on_event(self):
        async def handler(message: AbstractIncomingMessage) -> None:
            try:
                model = MessageData.model_validate_json(message.body.decode())
                await self._sender_func(model.to, model.topic, model.message)
            except Exception as e:
                logger.error(f"Error occured: {e}")
        return handler

    async def run(self):
        self._connection = await connect_robust(self._conn_url)
        self._channel = await self._connection.channel()
        self._queue = await self._channel.declare_queue(self._queue_name, durable=False)
        self._queue.consume(self._on_message(), no_ack=True)
        await self.keep()
