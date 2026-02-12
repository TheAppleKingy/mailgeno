from aiohttp import web

from pydantic import BaseModel

from .sender import send_mail
from .dto import MessageData
from .logger import logger


async def handle_http(request: web.Request):
    try:
        data = await request.json()
        model = MessageData.model_validate(data)
        await send_mail(model.to, model.topic, model.message)
    except Exception as e:
        logger.error(f"Error occured: {e}")
