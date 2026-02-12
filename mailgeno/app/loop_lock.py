import asyncio

from mailgeno.logger import logger


class LoopLockMixin:
    async def keep(self):
        while True:
            logger.info("Email sender up is working. Waiting for tasks")
            await asyncio.sleep(60*2)
