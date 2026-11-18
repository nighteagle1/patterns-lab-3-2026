from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from .formatter import MessageFormatter
from .logger import Logger
from .strategies import (
    ConsoleStrategy,
    FileStrategy,
    OutputStrategy,
    UpperFileStrategy,
)


class LoggerCreator(ABC):
    """Creator шаблона Factory Method.

    Метод ``create_logger`` использует фабричный метод ``create_strategy``,
    не зная, какая именно стратегия будет создана. Выбор конкретного класса
    делегирован подклассам.
    """

    @abstractmethod
    def create_strategy(self) -> OutputStrategy:
        """Фабричный метод: создаёт стратегию вывода."""

    def create_logger(self, formatter: MessageFormatter | None = None) -> Logger:
        return Logger(self.create_strategy(), formatter)


class ConsoleLoggerCreator(LoggerCreator):
    def create_strategy(self) -> OutputStrategy:
        return ConsoleStrategy()


class FileLoggerCreator(LoggerCreator):
    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)

    def create_strategy(self) -> OutputStrategy:
        return FileStrategy(self._path)


class UpperFileLoggerCreator(FileLoggerCreator):
    def create_strategy(self) -> OutputStrategy:
        return UpperFileStrategy(self._path)
