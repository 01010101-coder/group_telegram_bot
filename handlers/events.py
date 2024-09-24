from aiogram import Router

from aiogram.fsm.state import State, StatesGroup

from aiogram.fsm.context import FSMContext

from aiogram.filters import Command

from aiogram.types import Message

from db.users_db import UsersTable
from db.events import EventsTable

router = Router()
users_db = UsersTable()
events_db = EventsTable()


class GetEvent(StatesGroup):
    choosing_data = State()
    date = None
    time = None
    name = None
    description = None
    choosing_confirmation = State()


@router.message(Command(commands=['add_event']))
async def add_event(message: Message, state: FSMContext):
    await message.answer(
        text="Напиши дату, время, название и описание мероприятия через новую строку.",
    )
    await state.set_state(GetEvent.choosing_data)


@router.message(GetEvent.choosing_data)
async def process_data(message: Message, state: FSMContext):
    text = message.text.lower()
    data = text.split('\n') # ЗАМЕНИТЬ НА НОВУЮ СТРОКУ)
    await state.update_data(
        date=data[0],
        time=data[1],
        name=data[2],
        description=data[3]
    )
    await message.answer(
        text=f"Это правильно? \n{data}"
    )
    await state.set_state(GetEvent.choosing_confirmation)


@router.message(GetEvent.choosing_confirmation)
async def process_add_event(message: Message, state: FSMContext):
    text = message.text.lower()

    if text == "нет":
        await state.clear()
        await message.answer(
            text="Мероприятие не добавлено"
        )
        return

    data = await state.get_data()
    await events_db.add_event(data)
    await message.answer(
        text="Мероприятие добавлено"
    )
    await state.clear()
