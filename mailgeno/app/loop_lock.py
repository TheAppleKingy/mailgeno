import asyncio

from mailgeno.logger import logger


class LoopLockMixin:
    async def lock(self):
        try:
            while True:
                await asyncio.sleep(60*5)
                logger.info("mailgeno healthy")
        except asyncio.CancelledError:
            logger.info("mailgeno shutting down...")
