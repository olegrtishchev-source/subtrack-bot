import time
from loguru import logger
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

# Импортируем функцию обработки сообщений (её мы создадим следующим шагом)
# Пока она может подсвечиваться красным, это нормально, мы исправим это чуть позже.
from .handlers import process_message


def run_bot(token: str, group_id: int):
    """
    Запуск бота в режиме Long Polling.

    Args:
        token (str): Токен сообщества VK.
        group_id (int): ID сообщества (без минуса).
    """
    logger.info(f"🔌 Подключение к VK API (Group ID: {group_id})...")

    try:
        # Инициализация сессии VK
        vk_session = VkApi(token=token)

        # Инициализация Long Poll (сервер будет ждать сообщения и присылать их нам)
        longpoll = VkBotLongPoll(vk_session, group_id=group_id)

        # Получаем объект API для отправки сообщений
        vk = vk_session.get_api()

        logger.success("✅ Успешное подключение к VK Long Poll")
        logger.info("👂 Бот слушает сообщения... (Нажми Ctrl+C в консоли для остановки)")

        # БЕСКОНЕЧНЫЙ ЦИКЛ: Бот работает, пока мы его не остановим
        for event in longpoll.listen():
            # Нас интересуют только новые сообщения для бота
            if event.type == VkBotEventType.MESSAGE_NEW:
                message = event.object.message

                # Извлекаем важные данные из сообщения
                user_id = message["from_id"]  # Кто написал
                text = message["text"].strip()  # Что написал (убираем пробелы)
                peer_id = message["peer_id"]  # ID диалога (личка или чат)

                logger.info(f"💬 Сообщение от user_id={user_id}: '{text}'")

                # ПЕРЕДАЕМ СОБЩЕНИЕ В ОБРАБОТЧИК
                # Функция process_message решит, какую команду выполнить
                try:
                    process_message(vk, user_id, peer_id, text)
                except Exception as e:
                    logger.error(
                        f"Ошибка при обработке сообщения от {user_id}: {e}",
                        exc_info=True,
                    )
                    # Если случилась критическая ошибка в логике, стараемся не падать, а сообщить пользователю
                    vk.messages.send(
                        user_id=user_id,
                        message="❌ Произошла внутренняя ошибка. Попробуйте позже.",
                        random_id=int(time.time() * 1000),
                    )

    except Exception as e:
        logger.critical(f"💥 Критическая ошибка в цикле бота: {e}", exc_info=True)
        raise
