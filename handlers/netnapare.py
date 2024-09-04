from aiogram import Router, types
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from aiogram.filters import Command
from aiogram.filters import StateFilter

from aiogram import F

from db.users_db import UsersTable

router = Router()
users_db = UsersTable()


class GetData(StatesGroup):
    choosing_date = State()
    choosing_pairs = State()
    choosing_reason = State()


@router.message(StateFilter(None), Command(commands=['cancel']))
@router.message(StateFilter(None), F.text.lower() == 'стоп')
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    await state.set_data({})
    await message.answer(
        text="Нечего отменять",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command(commands=['cancel']))
@router.message(F.text.lower() == 'стоп')
async def cmd_cancel_in_state(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )


@router.callback_query(F.data == "net_na_pare")
async def start_accepting(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        text="Когда не будет?"
    )
    await state.set_state(GetData.choosing_date)


@router.message(GetData.choosing_date)
async def process_date(message: Message, state: FSMContext):
    await state.update_data(choosing_date=message.text.lower())
    await message.answer(
        text="На каких парах?(только номера)"
    )
    await state.set_state(GetData.choosing_pairs)


@router.message(GetData.choosing_pairs)
async def process_pairs(message: Message, state: FSMContext):
    await state.update_data(choosing_pairs=message.text.lower())
    await message.answer(
        text="Причина?"
    )
    await state.set_state(GetData.choosing_reason)


@router.message(GetData.choosing_reason)
async def process_reason(message: Message, state: FSMContext):
    await state.update_data(choosing_reason=message.text.lower())
    await message.answer(
        text="Готово"
    )
    await state.clear()
