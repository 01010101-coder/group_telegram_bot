import logging
from aiogram import Dispatcher, F

from aiogram.fsm.storage.memory import MemoryStorage

from middlewares import conf_middleware
from handlers import registration, netnapare, general, events
from handlers.notflications import schedule_pair_checks

from db.events import EventsTable
from db.users_db import UsersTable
from db.netnapare_db import SkipTable
from db.logs_db import LogsTable

from bot_instance import bot

logging.basicConfig(level=logging.INFO)

dp = Dispatcher(storage=MemoryStorage())

events_db = EventsTable()
users_db = UsersTable()
skip_db = SkipTable()
log_db = LogsTable()


async def on_startup():
    await users_db.initialize_table()
    await skip_db.initialize_table()
    await log_db.initialize_table()
    await events_db.initialize_table()

    schedule_pair_checks()


async def on_shutdown():
    await users_db.close()
    await skip_db.close()
    await log_db.close()
    await events_db.close()


async def main():
    await on_startup()

    dp.message.filter(F.text)
    dp.update.outer_middleware(conf_middleware.ConfirmationMiddleware())

    dp.include_router(netnapare.router)
    dp.include_router(registration.router)
    dp.include_router(events.router)
    dp.include_router(general.router)

    try:
        await dp.start_polling(bot)
    finally:
        await on_shutdown()
