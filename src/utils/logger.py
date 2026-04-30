import sys
import json
from pathlib import Path
from loguru import logger

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def setup_logging(debug_mode: bool = False):
    logger.remove()
    level = "DEBUG" if debug_mode else "INFO"

    # 1. Файловый лог (JSON) - используем serialize=True для надежности
    # Это встроенная функция loguru, она надежнее ручной
    logger.add(
        LOG_DIR / "bot.json",
        level=level,
        rotation="00:00",
        retention="7 days",
        compression="zip",
        serialize=True,  # <--- ВОЛШЕБСТВО: Loguru сама делает валидный JSON!
        enqueue=True,
    )

    # 2. Консоль
    if debug_mode:
        logger.add(
            sys.stderr,
            format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}:{line}</cyan> | <level>{message}</level>",
            level="DEBUG",
            enqueue=True,
        )
    else:
        logger.add(
            sys.stderr,
            format="{time:HH:mm:ss} | {level: <8} | {message}",
            level="INFO",
            enqueue=True,
        )

    logger.info("Логирование настроено")
