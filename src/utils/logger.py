from loguru import logger
import sys  # <-- ОБЯЗАТЕЛЬНО ДОБАВИТЬ ЭТУ СТРОКУ
import json
from pathlib import Path

from loguru import logger
import os
from pathlib import Path

# Создаём директорию для логов
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def setup_logging(debug_mode: bool = False):
    """
    Настройка логирования в JSON‑формате с ротацией по дням.

    Args:
        debug_mode (bool): если True — режим разработки (DEBUG), иначе — продакшен (INFO)
    """
    # Удаляем все существующие обработчики
    logger.remove()

    # Определяем уровень логирования
    log_level = "DEBUG" if debug_mode else "INFO"

    # Обработчик для JSON‑логов с ротацией
    logger.add(
        sink=LOG_DIR / "bot.json",
        format=lambda record: json.dumps(
            {
                "timestamp": record["time"].strftime("%Y-%m-%d %H:%M:%S"),
                "level": record["level"].name,
                "message": record["message"],
                "file": record["file"],
                "line": record["line"],
                "function": record["function"],
                **record["extra"],
            }
        ),
        rotation="00:00",
        retention="30 days",
        compression="zip",
        serialize=False,
        level=log_level,
        enqueue=True,
    )

    # Дополнительный обработчик для консоли (только в режиме разработки)
    if debug_mode:
        logger.add(
            sink=sys.stderr,
            format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}:{line}</cyan> - <level>{message}</level>",
            level="DEBUG",
            enqueue=True,
        )
        logger.debug("Режим разработки активирован")
    else:
        # В продакшене только базовые сообщения в консоль
        logger.add(
            sink=sys.stderr,
            format="{time:HH:mm:ss} | {level} | {message}",
            level="INFO",
            enqueue=True,
        )

    logger.info(
        f"Логирование настроено в режиме: {'РАЗРАБОТКА' if debug_mode else 'ПРОДАКШЕН'}"
    )
