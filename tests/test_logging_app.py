import re
from datetime import datetime
from pathlib import Path

import pytest

from logging_app import (
    ConsoleLoggerCreator,
    ConsoleStrategy,
    FileLoggerCreator,
    FileStrategy,
    InvalidLogLevelError,
    LogLevel,
    Logger,
    LoggerCreator,
    MessageFormatter,
    OutputStrategy,
    UpperFileLoggerCreator,
    UpperFileStrategy,
)

FIXED = datetime(2026, 3, 5, 9, 7, 3)


def fixed_formatter() -> MessageFormatter:
    return MessageFormatter(clock=lambda: FIXED)


# форматирование

def test_format_matches_required_pattern() -> None:
    result = fixed_formatter().format(LogLevel.INFO, "Hello")
    assert result == "2026-03-05 09:07:03 [INFO] Hello"


@pytest.mark.parametrize("level", list(LogLevel))
def test_format_supports_all_levels(level: LogLevel) -> None:
    assert f"[{level.value}] m" in fixed_formatter().format(level, "m")


def test_format_accepts_level_as_string() -> None:
    assert "[FATAL] boom" in fixed_formatter().format("FATAL", "boom")


# некорректный уровень

@pytest.mark.parametrize("bad", ["DEBUG", "info", "", None, 5])
def test_parse_rejects_invalid_level(bad: object) -> None:
    with pytest.raises(InvalidLogLevelError):
        LogLevel.parse(bad)


# стратегии

def test_console_strategy(capsys: pytest.CaptureFixture[str]) -> None:
    ConsoleStrategy().write("line")
    assert capsys.readouterr().out == "line\n"


def test_file_strategy_appends(tmp_path: Path) -> None:
    path = tmp_path / "app.log"
    strategy = FileStrategy(path)

    strategy.write("one")
    strategy.write("Two")

    assert path.read_text(encoding="utf-8") == "one\nTwo\n"


def test_file_strategy_creates_parent_directories(tmp_path: Path) -> None:
    path = tmp_path / "a" / "b" / "app.log"
    FileStrategy(path).write("x")
    assert path.read_text(encoding="utf-8") == "x\n"


def test_upper_file_strategy_uppercases(tmp_path: Path) -> None:
    path = tmp_path / "app.log"
    UpperFileStrategy(path).write("2026 [error] Something")
    assert path.read_text(encoding="utf-8") == "2026 [ERROR] SOMETHING\n"


# Logger (context)

class RecordingStrategy(OutputStrategy):
    def __init__(self) -> None:
        self.records: list[str] = []

    def write(self, text: str) -> None:
        self.records.append(text)


def test_logger_delegates_to_strategy_and_returns_formatted() -> None:
    strategy = RecordingStrategy()
    logger = Logger(strategy, fixed_formatter())

    result = logger.log(LogLevel.WARN, "careful")

    assert result == "2026-03-05 09:07:03 [WARN] careful"
    assert strategy.records == [result]


# фабричный метод

def test_creators_return_expected_strategy_types(tmp_path: Path) -> None:
    path = tmp_path / "app.log"
    assert isinstance(ConsoleLoggerCreator().create_strategy(), ConsoleStrategy)
    assert isinstance(FileLoggerCreator(path).create_strategy(), FileStrategy)
    assert isinstance(UpperFileLoggerCreator(path).create_strategy(), UpperFileStrategy)


def test_console_creator_logger_prints(capsys: pytest.CaptureFixture[str]) -> None:
    result = ConsoleLoggerCreator().create_logger(fixed_formatter()).log(LogLevel.INFO, "hello")
    assert capsys.readouterr().out == result + "\n"


def test_file_creator_logger_writes(tmp_path: Path) -> None:
    path = tmp_path / "app.log"
    FileLoggerCreator(path).create_logger(fixed_formatter()).log(LogLevel.WARN, "careful")
    assert path.read_text(encoding="utf-8") == "2026-03-05 09:07:03 [WARN] careful\n"


def test_upper_file_creator_logger_writes_uppercase(tmp_path: Path) -> None:
    path = tmp_path / "app.log"
    UpperFileLoggerCreator(path).create_logger(fixed_formatter()).log(LogLevel.ERROR, "oops")
    assert path.read_text(encoding="utf-8") == "2026-03-05 09:07:03 [ERROR] OOPS\n"
