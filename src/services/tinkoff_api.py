from utils.logger import logger


async def get_transactions(access_token: str, account_id: str):
    try:
        logger.debug(f"Запрос транзакций для аккаунта {account_id}")
        # ... код запроса
        logger.info(f"Получено {len(transactions)} транзакций")
        return transactions
    except Exception as e:
        logger.error(f"Ошибка получения транзакций: {e}")
        raise
