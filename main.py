import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from dotenv import load_dotenv
import os
from aiogram.fsm.storage.memory import MemoryStorage

from middlewares import conf_middleware
from handlers import registration, netnapare, general
from db.users_db import UsersTable
from db.netnapare_db import SkipTable

logging.basicConfig(level=logging.INFO)

load_dotenv('settings.env')

bot_token = os.getenv("BOT_TOKEN")

if not bot_token:
    raise ValueError("Токен бота не найден. Проверьте файл settings.env.")

# Инициализация бота и диспетчера
bot = Bot(token=bot_token)
dp = Dispatcher(storage=MemoryStorage())

users_db = UsersTable()
skip_db = SkipTable()


async def on_startup():
    await users_db.initialize_table()
    await skip_db.initialize_table()


async def on_shutdown():
    await users_db.close()
    await skip_db.close()


async def main():
    await on_startup()

    dp.message.filter(F.text)
    dp.update.outer_middleware(conf_middleware.ConfirmationMiddleware())

    dp.include_router(netnapare.router)
    dp.include_router(registration.router)
    dp.include_router(general.router)

    try:
        await dp.start_polling(bot)
    finally:
        await on_shutdown()
