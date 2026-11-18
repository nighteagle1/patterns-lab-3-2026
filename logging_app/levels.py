from __future__ import annotations

from enum import Enum


class InvalidLogLevelError(ValueError):
    """Передан уровень сообщения, которого нет среди допустимых."""


class LogLevel(str, Enum):
    TRACE = "TRACE"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    FATAL = "FATAL"

    @classmethod
    def parse(cls, value: object) -> LogLevel:
        """Приводит значение к LogLevel или выбрасывает InvalidLogLevelError.

        Принимается сам LogLevel либо строка с точным названием уровня
        (например, "INFO"). Всё остальное считается ошибкой.
        """
        if isinstance(value, cls):
            return value
        if isinstance(value, str):
            try:
                return cls(value)
            except ValueError:
                pass
        allowed = ", ".join(level.value for level in cls)
        raise InvalidLogLevelError(
            f"Недопустимый уровень сообщения: {value!r}. Допустимые: {allowed}"
        )
