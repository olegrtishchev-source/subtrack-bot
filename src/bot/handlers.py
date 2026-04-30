import asyncio
import time
from loguru import logger
from vk_api import VkApi
from typing import List

from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def get_main_keyboard() -> dict:
    """
    Создает основную клавиатуру с кнопками.
    Возвращает словарь в формате, который понимает VK API.
    """
    keyboard = VkKeyboard(
        one_time=False
    )  # one_time=False значит клавиатура не исчезнет после нажатия

    # Первый ряд
    keyboard.add_button("💰 Самая дорогая", color=VkKeyboardColor.POSITIVE)  # Зеленая
    keyboard.add_button("📉 Самая дешевая", color=VkKeyboardColor.NEGATIVE)  # Красная

    # Второй ряд
    keyboard.add_button("📜 История", color=VkKeyboardColor.SECONDARY)  # Серая
    keyboard.add_button("❓ Помощь", color=VkKeyboardColor.SECONDARY)

    return keyboard.get_keyboard()


# Импорты наших сервисов и моделей
# Обратите внимание: мы импортируем из соседних папок через относительные пути или через src
from src.services.bank_api import MockBankAPI, BankConnectionError
from src.models.database import User, Subscription, RequestHistory

# Создаем экземпляр нашего Mock-сервиса
bank_api = MockBankAPI()


def get_or_create_user(vk_id: int) -> User:
    """
    Находит пользователя в БД или создает нового.
    """
    user, created = User.get_or_create(vk_id=str(vk_id))
    if created:
        logger.info(f"🆕 Новый пользователь зарегистрирован: {vk_id}")
    return user


def send_message(vk: VkApi, user_id: int, message: str, keyboard: dict = None):
    """
    Отправляет сообщение, опционально с клавиатурой.
    """
    params = {
        "user_id": user_id,
        "message": message,
        "random_id": int(time.time() * 1000),
    }

    if keyboard:
        params["keyboard"] = keyboard

    try:
        vk.messages.send(**params)
        logger.debug(f"📤 Сообщение отправлено пользователю {user_id}")
    except Exception as e:
        logger.error(f"❌ Не удалось отправить сообщение: {e}")


def handle_start(vk: VkApi, user_id: int):
    """Команда /start"""
    user = get_or_create_user(user_id)
    text = (
        f"Привет! Я SubTrack Bot 🤖\n"
        f"Я помогу тебе следить за подписками.\n\n"
        f"Выбери действие в меню ниже:"
    )
    # Отправляем с клавиатурой
    send_message(vk, user_id, text, keyboard=get_main_keyboard())


def handle_help(vk: VkApi, user_id: int):
    """Команда /help"""
    text = (
        "📚 **Справка:**\n"
        "Нажимай на кнопки ниже, чтобы узнать о своих подписках.\n\n"
        "💰 **Дорогая** — покажет самую затратную подписку.\n"
        "📉 **Дешевая** — покажет самую экономную.\n"
        "📜 **История** — покажет последние 5 запросов."
    )
    send_message(vk, user_id, text, keyboard=get_main_keyboard())


def handle_high(vk: VkApi, user_id: int):
    """Команда /high - самая дорогая подписка"""
    user = get_or_create_user(user_id)

    try:
        # Запускаем асинхронную функцию внутри синхронной
        subscriptions: List = asyncio.run(bank_api.get_subscriptions(user_id))

        if not subscriptions:
            send_message(vk, user_id, "У вас пока нет активных подписок.")
            return

        # Ищем самую дорогую
        most_expensive = max(subscriptions, key=lambda x: x.cost)

        text = (
            f"💰 **Самая дорогая подписка:**\n"
            f"Сервис: {most_expensive.name}\n"
            f"Цена: {most_expensive.cost} {most_expensive.currency}\n"
            f"Дата оплаты: {most_expensive.next_payment_date.strftime('%d.%m.%Y')}\n\n"
            f"Логотип: {most_expensive.icon_url}"
        )

        # Сохраняем в историю
        RequestHistory.create(
            user=user,
            command="/high",
            result_summary=f"Max: {most_expensive.name} ({most_expensive.cost})",
        )

        send_message(vk, user_id, text)
        logger.success(f"✅ Команда /high выполнена для {user_id}")

    except BankConnectionError:
        send_message(
            vk, user_id, "⚠️ Ошибка: Временные проблемы с банком. Попробуйте позже."
        )
        logger.warning("⚠️ Ошибка соединения с банком при /high")
    except Exception as e:
        send_message(vk, user_id, "❌ Произошла ошибка при обработке запроса.")
        logger.error(f"❌ Ошибка в /high: {e}", exc_info=True)


def handle_low(vk: VkApi, user_id: int):
    """Команда /low - самая дешевая подписка"""
    user = get_or_create_user(user_id)

    try:
        subscriptions: List = asyncio.run(bank_api.get_subscriptions(user_id))

        if not subscriptions:
            send_message(vk, user_id, "У вас пока нет активных подписок.")
            return

        # Ищем самую дешевую
        cheapest = min(subscriptions, key=lambda x: x.cost)

        text = (
            f"📉 **Самая дешевая подписка:**\n"
            f"Сервис: {cheapest.name}\n"
            f"Цена: {cheapest.cost} {cheapest.currency}\n"
            f"Дата оплаты: {cheapest.next_payment_date.strftime('%d.%m.%Y')}\n\n"
            f"Логотип: {cheapest.icon_url}"
        )

        RequestHistory.create(
            user=user,
            command="/low",
            result_summary=f"Min: {cheapest.name} ({cheapest.cost})",
        )

        send_message(vk, user_id, text)
        logger.success(f"✅ Команда /low выполнена для {user_id}")

    except BankConnectionError:
        send_message(
            vk, user_id, "⚠️ Ошибка: Временные проблемы с банком. Попробуйте позже."
        )
    except Exception as e:
        send_message(vk, user_id, "❌ Произошла ошибка при обработке запроса.")
        logger.error(f"❌ Ошибка в /low: {e}", exc_info=True)


def handle_history(vk: VkApi, user_id: int):
    """Команда /history - история запросов"""
    user = get_or_create_user(user_id)

    # Берем последние 5 записей из БД
    history = (
        RequestHistory.select()
        .where(RequestHistory.user == user)
        .order_by(RequestHistory.timestamp.desc())
        .limit(5)
    )

    if not history:
        send_message(
            vk, user_id, "📭 История пуста. Вы еще не использовали команды поиска."
        )
        return

    text = "📜 **Ваши последние запросы:**\n\n"
    for record in history:
        time_str = record.timestamp.strftime("%d.%m %H:%M")
        text += f"⏰ {time_str} | {record.command} ➡️ {record.result_summary}\n"

    send_message(vk, user_id, text)


def process_message(vk: VkApi, user_id: int, peer_id: int, text: str):
    """
    ГЛАВНЫЙ ДИСПЕТЧЕР.
    Теперь умеет приветствовать новых пользователей автоматически.
    """
    text = text.strip()
    text_lower = text.lower()

    # Проверяем, есть ли пользователь в базе
    # Если пользователя нет, считаем это первым запуском
    user_exists = User.select().where(User.vk_id == str(user_id)).exists()

    # Если пользователь новый И сообщение пустое (или системное) ИЛИ явно написано "начать"
    # Мы отправляем приветствие
    if not user_exists and (
        text_lower == ""
        or text_lower == "начать"
        or text_lower == "/start"
        or text_lower == "start"
    ):
        logger.info(f"Новый пользователь {user_id}. Отправляем авто-приветствие.")
        handle_start(vk, user_id)
        return

    # Стандартная логика команд
    if text_lower == "/start" or text_lower == "начать" or text_lower == "start":
        handle_start(vk, user_id)

    elif text_lower == "/help" or text == "❓ Помощь":
        handle_help(vk, user_id)

    elif text == "💰 Самая дорогая" or text_lower == "/high":
        handle_high(vk, user_id)

    elif text == "📉 Самая дешевая" or text_lower == "/low":
        handle_low(vk, user_id)

    elif text == "📜 История" or text_lower == "/history":
        handle_history(vk, user_id)

    else:
        # Если пользователь написал что-то непонятное, но он уже не новый
        # Предлагаем воспользоваться кнопками
        send_message(
            vk,
            user_id,
            "🤔 Я не понял команду. Воспользуйтесь кнопками внизу!",
            keyboard=get_main_keyboard(),
        )
