import asyncio

from src.logger import logger


class LoopLockMixin:
    async def keep(self):
        try:
            while True:
                await asyncio.sleep(60*2)
                logger.info("mailgeno healthy")
        except asyncio.CancelledError:
            logger.info("mailgeno shutting down...")
