import os
from dotenv import load_dotenv
from loguru import logger

# Загружаем переменные из .env (только если файл существует)
if os.path.exists(".env"):
    load_dotenv()
else:
    logger.warning("Файл .env не найден! Убедитесь, что он существует в корне проекта.")

# Конфигурация VK Bot
VK_BOT_TOKEN = os.getenv("VK_BOT_TOKEN")
# GROUP_ID должен быть числом. В .env пиши просто цифры, без минуса и кавычек.
GROUP_ID_RAW = os.getenv("GROUP_ID")

if GROUP_ID_RAW:
    try:
        GROUP_ID = int(GROUP_ID_RAW)
    except ValueError:
        logger.error("GROUP_ID должен быть числом! Проверь файл .env")
        GROUP_ID = None
else:
    GROUP_ID = None

# --- Конфигурация БД ---
# Для SQLite достаточно имени файла
DB_NAME = os.getenv("DB_NAME", "subtrack_bot.db")

# --- Конфигурация Redis (пока не используется, но пусть будет) ---
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# --- Режим отладки ---
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"

# --- Логирование конфигурации (для проверки) ---
# В продакшене токены лучше не логировать, но для учебы полезно видеть, что загрузилось
if DEBUG_MODE:
    logger.debug(
        f"Config loaded: VK_TOKEN={'***' if VK_BOT_TOKEN else 'MISSING'}, GROUP_ID={GROUP_ID}"
    )
