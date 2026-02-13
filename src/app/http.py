import asyncio

from urllib.parse import urlparse

from aiohttp import web

from src.logger import logger
from src.app.base import AbstractEmailSenderApp
from .loop_lock import LoopLockMixin


class HttpEmailSenderApp(AbstractEmailSenderApp, LoopLockMixin):
    def __init__(self, conn_url: str, listen_for: str):
        super().__init__(conn_url, listen_for)
        self._app: web.Application = None
        self._runner: web.AppRunner = None
        self._site: web.TCPSite = None

    async def validate_data(self, data: web.Request) -> dict[str, str]:
        return await data.json()

    def return_func(self, ok: bool):
        if ok:
            return web.json_response({"detail": "Email sent"})
        return web.json_response({"error": "Email was not sent. See logs"})

    async def run(self):
        self._app = web.Application()
        self._app.router.add_post(f"/{self._listen_for}", self.on_event())
        self._runner = web.AppRunner(self._app)
        await self._runner.setup()
        res = urlparse(self._conn_url)
        port = int(res.netloc.split(":")[-1])
        self._site = web.TCPSite(self._runner, host="0.0.0.0", port=port)
        await self._site.start()
        logger.info("HttpEmailSenderApp started. Ready to accept requests")
        await self.keep()
