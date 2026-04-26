import sys
from config import VK_BOT_TOKEN, DEBUG_MODE
from utils.logger import setup_logging
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

# Настройка логирования
setup_logging(debug_mode=DEBUG_MODE)

# Инициализация API
vk_session = VkApi(token=VK_BOT_TOKEN)
longpoll = VkBotLongPoll(vk_session, group_id=123456789)  # замените на ID вашей группы
vk = vk_session.get_api()

logger.debug(f"Токен бота загружен: {VK_BOT_TOKEN[:10]}...")
logger.info("Запуск бота SubTrack Bot")


def main():
    logger.info("Бот запущен и готов к работе")
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            message = event.object.message
            logger.info(
                f"Пользователь {message['from_id']} отправил сообщение: {message['text']}"
            )
            # Обработка команд
            if message["text"].lower() == "start":
                vk.messages.send(
                    user_id=message["from_id"],
                    message="Привет! Бот запущен!",
                    random_id=0,
                )


if __name__ == "__main__":
    main()
