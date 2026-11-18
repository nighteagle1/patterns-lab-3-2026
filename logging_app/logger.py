from __future__ import annotations

from .formatter import MessageFormatter
from .levels import LogLevel
from .strategies import OutputStrategy


class Logger:
    """Context шаблона Strategy.

    Форматирует сообщение и делегирует вывод переданной стратегии.
    Не знает конкретных стратегий и не создаёт их.
    """

    def __init__(
        self,
        strategy: OutputStrategy,
        formatter: MessageFormatter | None = None,
    ) -> None:
        self._strategy = strategy
        self._formatter = formatter or MessageFormatter()

    def log(self, level: LogLevel | str, message: str) -> str:
        formatted = self._formatter.format(level, message)
        self._strategy.write(formatted)
        return formatted
