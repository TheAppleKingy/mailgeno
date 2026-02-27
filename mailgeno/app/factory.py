from urllib.parse import urlparse

from mailgeno.app.base import AbstractEmailSenderApp
from mailgeno.app.http import HttpEmailSenderApp
from mailgeno.app.rabbit import RabbitEmailSenderApp


class AppFactory:
    def __init__(self, conn_url: str, listen_for: str):
        self._conn_url = conn_url
        self._listen_for = listen_for
        self._app_map: dict[str, type[AbstractEmailSenderApp]] = {
            "http": HttpEmailSenderApp,
            "amqp": RabbitEmailSenderApp
        }

    def get_app(self):
        res = urlparse(self._conn_url)
        app = self._app_map.get(res.scheme)
        if not app:
            raise KeyError(f"App for protocol scheme '{res.scheme}' was not registered")
        return app(self._conn_url, self._listen_for)
