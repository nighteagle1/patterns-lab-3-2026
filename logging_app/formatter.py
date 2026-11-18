from __future__ import annotations

from datetime import datetime
from typing import Callable

from .levels import LogLevel

Clock = Callable[[], datetime]


class MessageFormatter:
    """Формирует строку вида ``YYYY-MM-DD HH:mm:ss [LEVEL] Message``.

    Источник времени можно подменить (``clock``), чтобы тесты не зависели
    от текущего времени.
    """

    TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, clock: Clock = datetime.now) -> None:
        self._clock = clock

    def format(self, level: LogLevel | str, message: str) -> str:
        parsed = LogLevel.parse(level)
        timestamp = self._clock().strftime(self.TIME_FORMAT)
        return f"{timestamp} [{parsed.value}] {message}"
