import aiosmtplib
import asyncio

from typing import Callable, Awaitable
from email.message import EmailMessage

from .config import conf
from .logger import logger


MAX_RETRIES = 5


def _build_message(
    to: str,
    topic: str,
    text: str
) -> EmailMessage:
    message = EmailMessage()
    message['From'] = conf.sender
    message['To'] = to
    message['Subject'] = topic
    message.set_content(text)
    return message


async def _send_task(msg: EmailMessage):
    async with aiosmtplib.SMTP(hostname=conf.host, port=conf.port, use_tls=True) as cli:
        await cli.login(conf.sender, conf.password)
        try:
            await cli.send_message(msg)
            logger.info(f"Email with topic '{msg['Subject']}' sent to '{msg['To']}'")
        except Exception as e:
            logger.error(
                f"Unable to send email with topic '{msg['Subject']}' to '{msg["To"]}': {e}")


async def send_mail(
    to: str,
    topic: str,
    text: str
):
    task = _send_task(_build_message(to, topic, text))
    for i in range(1, MAX_RETRIES + 1):
        try:
            await task
            logger.info(f"Email sent to '{to}'. Topic: '{topic}'")
            return None
        except Exception as e:
            logger.error(f"Error occured when send mail to '{to}': {e}. Was attempt {i}/{MAX_RETRIES}")
    logger.error(f"Email from '{to}' with topic '{topic}' was not send")
