import asyncio
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import netnapare

from middlewares import conf_middleware
from handlers import registration
from db import UsersTable

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Загрузка переменных из settings.env
load_dotenv('settings.env')

# Получение токена из переменных окружения
bot_token = os.getenv("BOT_TOKEN")

if not bot_token:
    raise ValueError("Токен бота не найден. Проверьте файл settings.env.")

# Инициализация бота и диспетчера
bot = Bot(token=bot_token)
dp = Dispatcher(storage=MemoryStorage())

# Создание одного экземпляра UsersTable
users_db = UsersTable()


# Инициализация таблицы базы данных при старте приложения
async def on_startup():
    await users_db.initialize_table()


# Закрытие соединения при завершении работы приложения
async def on_shutdown():
    await users_db.close()


async def main():
    # Вызов инициализации таблицы при старте
    await on_startup()

    dp.update.outer_middleware(conf_middleware.ConfirmationMiddleware())
    dp.include_router(registration.router)
    dp.include_router(netnapare.router)

    try:
        await dp.start_polling(bot)
    finally:
        await on_shutdown()

if __name__ == "__main__":
    asyncio.run(main())
