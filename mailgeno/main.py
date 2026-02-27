import asyncio

import click

from mailgeno.logger import logger
from mailgeno.app.factory import AppFactory


@click.command()
@click.option("-c", "--conn_url", default="http://localhost:8052", type=str, help="Listening web interface or brocker connect URL")
@click.option("-r", "--resource", default="mail", help="Resource that app shpould to listen")
def main(conn_url: str, resource: str):
    factory = AppFactory(conn_url, resource)
    try:
        app = factory.get_app()
    except Exception as e:
        logger.error(f"Unable to resolve app: {e}")
        return
    logger.info("mailgeno app starting")
    asyncio.run(app.run())


if __name__ == "__main__":
    main()
