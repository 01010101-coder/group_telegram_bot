import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import load_dotenv
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Загрузка переменных из settings.env
load_dotenv('settings.env')

# Получение токена из переменных окружения
bot_token = os.getenv("BOT_TOKEN")

if not bot_token:
    raise ValueError("Токен бота не найден. Проверьте файл settings.env.")

bot = Bot(token=bot_token)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
