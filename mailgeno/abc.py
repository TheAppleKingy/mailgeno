from typing import Callable, Awaitable
from abc import ABC, abstractmethod
from urllib.parse import urlparse

SenderType = Callable[[str, str, str], Awaitable[None]]
