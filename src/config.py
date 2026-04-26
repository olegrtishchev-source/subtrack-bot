import os
from dotenv import load_dotenv

# Загружаем переменные из .env (только если файл существует)
if os.path.exists(".env"):
    load_dotenv()

# Конфигурация VK Bot
VK_BOT_TOKEN = os.getenv("VK_BOT_TOKEN")

# Конфигурация Tinkoff API
TINKOFF_CLIENT_ID = os.getenv("TINKOFF_CLIENT_ID")
TINKOFF_CLIENT_SECRET = os.getenv("TINKOFF_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# Конфигурация БД
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///subtrack.db")

# Конфигурация Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# Конфигурация Sentry
SENTRY_DSN = os.getenv("SENTRY_DSN")

# Режим отладки
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
