import asyncio
import random
from datetime import datetime, timedelta
from typing import List, Optional
from abc import ABC, abstractmethod
from loguru import logger


class BankConnectionError(Exception):
    """Ошибка соединения с банковским API"""

    pass


class SubscriptionData:
    """Модель данных подписки."""

    def __init__(
        self,
        name: str,
        cost: float,
        currency: str,
        icon_url: str,
        next_payment_date: datetime,
    ):
        self.name = name
        self.cost = cost
        self.currency = currency
        self.icon_url = icon_url
        self.next_payment_date = next_payment_date

    def __repr__(self):
        return f"<Subscription {self.name}: {self.cost} {self.currency}>"


class BaseBankAPI(ABC):
    """
    Абстрактный базовый класс для банковского API.
    Реализует принцип инверсии зависимостей (Dependency Inversion Principle).
    """

    @abstractmethod
    async def get_subscriptions(self, user_id: int) -> List[SubscriptionData]:
        """
        Получает список активных подписок пользователя.

        Args:
            user_id (int): ID пользователя в системе банка.

        Returns:
            List[SubscriptionData]: Список объектов подписок.

        Raises:
            BankConnectionError: Если не удалось соединиться с банком.
        """
        pass


class MockBankAPI(BaseBankAPI):
    """
    Имитация банковского API (Mock Server).
    Возвращает фиктивные данные с эмуляцией задержек и ошибок.
    """

    # Фиктивные данные. В реальном проекте это приходило бы из БД или внешнего API.
    _mock_data: dict[int, List[SubscriptionData]] = {
        1: [
            SubscriptionData(
                "Яндекс.Плюс",
                299.0,
                "RUB",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Yandex_Plus_logo.svg/1200px-Yandex_Plus_logo.svg.png",
                datetime.now() + timedelta(days=2),
            ),
            SubscriptionData(
                "Netflix",
                15.99,
                "USD",
                "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg",
                datetime.now() + timedelta(days=5),
            ),
            SubscriptionData(
                "Spotify",
                199.0,
                "RUB",
                "https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg",
                datetime.now() + timedelta(days=10),
            ),
        ],
        2: [
            SubscriptionData(
                "VK Музыка",
                169.0,
                "RUB",
                "https://upload.wikimedia.org/wikipedia/commons/2/21/VK_Compact_Logo_%282021-present%29.svg",
                datetime.now() + timedelta(days=1),
            ),
            SubscriptionData(
                "GitHub Pro",
                4.0,
                "USD",
                "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
                datetime.now() + timedelta(days=20),
            ),
        ],
    }

    async def get_subscriptions(self, user_id: int) -> List[SubscriptionData]:
        logger.info(f"Запрос подписок для user_id={user_id}")

        # 1. Эмуляция сетевой задержки
        delay = random.uniform(0.5, 1.5)
        await asyncio.sleep(delay)

        # 2. Эмуляция редкой ошибки (5% шанс)
        if random.random() < 0.05:
            logger.error("Эмитирована ошибка соединения с банком")
            raise BankConnectionError(
                "Временные проблемы с соединением банка. Попробуйте позже."
            )

        # 3. Логика получения данных (ИСПРАВЛЕННАЯ)
        # Пытаемся получить данные для конкретного пользователя
        subscriptions = self._mock_data.get(user_id)

        # Если данных нет, берем демо-набор (пользователь №1)
        if subscriptions is None:
            logger.info(f"Пользователь {user_id} не найден. Возвращаем демо-данные.")
            subscriptions = self._mock_data.get(1)

        # На всякий случай: если вдруг и пользователь №1 не найден (что невозможно при нашей структуре),
        # возвращаем пустой список, а не None, чтобы не было ошибок итерации
        if subscriptions is None:
            return []

        logger.success(f"Найдено {len(subscriptions)} подписок для user_id={user_id}")
        return subscriptions
