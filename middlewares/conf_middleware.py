from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram import Bot

from db.users_db import UsersTable

users_db = UsersTable()


class ConfirmationMiddleware(BaseMiddleware):
    async def __call__(self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        tg_id = data['event_from_user'].id
        user = await users_db.get_user_by_tg_id(tg_id)
        bot: Bot = data['bot']  

        if user is None:
            await bot.send_message(chat_id=tg_id, text="Напиши /start, чтобы зарегистрироваться")
            return

        if user[4] == 0:
            await bot.send_message(chat_id=tg_id, text="Тебя еще не подтвердили")
            return

        return await handler(event, data)
