from logging_app import (
    ConsoleLoggerCreator,
    FileLoggerCreator,
    LogLevel,
    UpperFileLoggerCreator,
)

LOG_FILE = "logs/app.log"


def main() -> None:
    ConsoleLoggerCreator().create_logger().log(LogLevel.INFO, "Application started")
    FileLoggerCreator(LOG_FILE).create_logger().log(LogLevel.WARN, "Low disk space")
    UpperFileLoggerCreator(LOG_FILE).create_logger().log(LogLevel.ERROR, "Example error")


if __name__ == "__main__":
    main()
