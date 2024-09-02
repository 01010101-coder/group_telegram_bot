from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.callback_data import CallbackData
from typing import Optional

from aiogram import F

from keyboards.general_keyboards import main_menu_keyboard
from db import UsersTable

router = Router()
users_db = UsersTable()

class GetData(StatesGroup):
    choosing_date = State()
    choosing_pairs = State()
    choosing_reason = State()


@router.callback_query(F.data == "net_na_pare")
async def start_accepting(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(
        text="Когда не будет?"
    )
    await state.set_state(GetData.choosing_date)
