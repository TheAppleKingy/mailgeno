import asyncio
from aiohttp import web

from .controllers import handle_http
from .config import conf


def get_app(protocol: str):
    pass


async def main():
    app = web.Application()
