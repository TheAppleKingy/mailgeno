import asyncio
from typing import NewType
from aiohttp import web


from mailgeno.logger import logger
from mailgeno.sender import send_mail
from mailgeno.dto import MessageData
from .base import AbstractEmailSenderApp
from .loop_lock import LoopLockMixin

IncomingData = NewType("IncomingData")


class HttpEmailSenderApp(AbstractEmailSenderApp):
    def __init__(self, conn_url: str):
        super().__init__(conn_url)
        self._app: web.Application = None

    def _validate_json(self, request: web.Request):
        return asyncio.run(request.json())

    def _on_event(self):
        async def handler(request: web.Request):
            try:
                model = MessageData.model_validate(await request.json())
                await send_mail(model.to, model.topic, model.message)
                return web.json_response({"detail": "Email sent"})
            except Exception as e:
                logger.error(f"Error occured: {e}")
                return web.json_response({"error": "Email was not sent. See logs"}, status=500)
        return handler

    async def run(self):
        self._app = web.Application(logger=logger)
        self._app.router.add_post("/send_mail", self._on_event)
