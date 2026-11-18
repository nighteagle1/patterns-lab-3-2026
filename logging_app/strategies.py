from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from pathlib import Path


class OutputStrategy(ABC):
    """Strategy: общий интерфейс способа вывода готовой строки."""

    @abstractmethod
    def write(self, text: str) -> None:
        """Выводит уже отформатированную строку."""


class ConsoleStrategy(OutputStrategy):
    """Вывод в консоль."""

    def write(self, text: str) -> None:
        print(text, file=sys.stdout)


class FileStrategy(OutputStrategy):
    """Дозапись строки в текстовый файл."""

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)

    @property
    def path(self) -> Path:
        return self._path

    def write(self, text: str) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("a", encoding="utf-8") as stream:
            stream.write(text + "\n")


class UpperFileStrategy(FileStrategy):
    """Запись в файл с преобразованием всей строки в верхний регистр."""

    def write(self, text: str) -> None:
        super().write(text.upper())
