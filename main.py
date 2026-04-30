import sys
from loguru import logger

# Импорты из наших модулей
from src.config import VK_BOT_TOKEN, DEBUG_MODE, GROUP_ID
from src.utils.logger import setup_logging
from src.models.database import init_db
from src.bot.runner import run_bot  # <--- Импортируем нашу новую функцию


def main():
    # 1. Настройка логирования
    setup_logging(debug_mode=DEBUG_MODE)

    logger.info("🚀 Запуск SubTrack Bot...")

    # 2. Проверка токена и ID
    if not VK_BOT_TOKEN:
        logger.error("❌ Ошибка: VK_BOT_TOKEN не найден в .env файле!")
        sys.exit(1)

    if not GROUP_ID:
        logger.error("❌ Ошибка: GROUP_ID не найден в .env файле!")
        sys.exit(1)

    # 3. Инициализация базы данных
    try:
        init_db()
        logger.success("✅ База данных готова к работе")
    except Exception as e:
        logger.critical(f"❌ Критическая ошибка БД: {e}")
        sys.exit(1)

    # 4. ЗАПУСК БОТА
    logger.info("🔄 Запускаем цикл обработки сообщений...")
    try:
        run_bot(VK_BOT_TOKEN, GROUP_ID)
    except KeyboardInterrupt:
        logger.info("👋 Бот остановлен пользователем (Ctrl+C)")
    except Exception as e:
        logger.critical(f"Бот упал с ошибкой: {e}")


if __name__ == "__main__":
    main()
