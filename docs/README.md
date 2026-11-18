# Диаграмма

Структурная диаграмма решения (Mermaid): [diagram.md](diagram.md).

Участники шаблонов:

- **Strategy**: `OutputStrategy` (интерфейс), `ConsoleStrategy`, `FileStrategy`, `UpperFileStrategy` (конкретные стратегии), `Logger` (контекст).
- **Factory Method**: `LoggerCreator` (создатель с фабричным методом `create_strategy()`), `ConsoleLoggerCreator`, `FileLoggerCreator`, `UpperFileLoggerCreator` (конкретные создатели).
