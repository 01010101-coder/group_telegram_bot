from aiogram import Bot
import os
from dotenv import load_dotenv

load_dotenv('settings.env')

bot_token = os.getenv("BOT_TOKEN")

if not bot_token:
    raise ValueError("Токен бота не найден. Проверьте файл settings.env.")

# Инициализация бота
bot = Bot(token=bot_token)
