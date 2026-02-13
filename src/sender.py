import aiosmtplib
import asyncio

from email.message import EmailMessage

from src.config import conf
from src.logger import logger


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


async def _call_send(msg: EmailMessage):
    async with aiosmtplib.SMTP(hostname=conf.host, port=conf.port, use_tls=True) as cli:
        await cli.login(conf.sender, conf.password)
        await cli.send_message(msg)


async def _send_task(msg: EmailMessage):
    for i in range(1, MAX_RETRIES + 1):
        try:
            await _call_send(msg)
            logger.info(f"Email with topic '{msg['Subject']}' sent to '{msg['To']}'")
            return None
        except Exception as e:
            logger.error(f"{i}/{MAX_RETRIES} error occured when send mail to '{msg["To"]}': {e}")
    logger.error(f"Email to '{msg["To"]}' with topic '{msg["Subject"]}' was not send")


def send_mail(
    to: str,
    topic: str,
    text: str
):
    asyncio.create_task(_send_task(_build_message(to, topic, text)))
