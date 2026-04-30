from peewee import (
    Model,
    SqliteDatabase,
    CharField,
    FloatField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
)
from datetime import datetime
from loguru import logger

# Подключаемся к той же БД, что и раньше
db = SqliteDatabase("subtrack_bot.db")


class User(Model):
    """
    Модель пользователя бота.
    Хранит ID пользователя из ВКонтакте.
    """

    vk_id = CharField(
        unique=True, index=True
    )  # Уникальный ID из VK, индекс для быстрого поиска
    created_at = DateTimeField(default=datetime.now)  # Дата регистрации

    class Meta:
        database = db  # Указываем, к какой БД относится модель


class Subscription(Model):
    """
    Модель подписки.
    Хранит информацию о сервисе, на который подписан пользователь.
    """

    user = ForeignKeyField(User, backref="subscriptions", on_delete="CASCADE")
    name = CharField()  # Название сервиса (Netflix, Яндекс.Плюс)
    cost = FloatField()  # Стоимость
    currency = CharField(default="RUB")  # Валюта
    next_payment = DateTimeField()  # Дата следующего списания
    logo_url = CharField(null=True)  # Ссылка на логотип (может быть пустой)

    class Meta:
        database = db


class RequestHistory(Model):
    """
    Модель истории запросов.
    Нужна для команды /history.
    """

    user = ForeignKeyField(User, backref="history", on_delete="CASCADE")
    command = CharField()  # Какую команду ввел пользователь (/high, /low)
    result_summary = CharField(max_length=255)  # Краткое описание результата
    timestamp = DateTimeField(default=datetime.now)  # Время запроса

    class Meta:
        database = db


def init_db():
    """
    Инициализация базы данных: подключение и создание таблиц.
    """
    try:
        db.connect()
        # Создаем таблицы, если их нет (safe=True)
        db.create_tables([User, Subscription, RequestHistory], safe=True)
        logger.info(
            "База данных инициализирована. Таблицы: User, Subscription, RequestHistory"
        )
    except Exception as e:
        logger.error(f"Ошибка при инициализации БД: {e}")
        raise
    finally:
        if not db.is_closed():
            db.close()
