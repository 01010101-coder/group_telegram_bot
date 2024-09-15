from aiogram import Router, types
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.general_keyboards import choose_enter_method, is_correct_keyboard

from filters.date_check import parse_date
from filters.lessons_check import parse_lessons

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


class GetDataGpt(StatesGroup):
    choosing_text = State()


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
async def choose_method(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        text="Как вводить данные?",
        reply_markup=choose_enter_method()
    )


@router.callback_query(F.data == "gpt_enter")
async def gpt_method(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        text="Напиши полное сообщение когда тебя не будет, на каких парах и причину"
    )
    await state.set_state(GetDataGpt.choosing_text)


@router.message(GetDataGpt.choosing_text)
async def process_text(message: Message, state: FSMContext):
    await message.answer(
        text=message.text.lower()
    )
    await state.clear()


@router.callback_query(F.data == "manually_enter")
async def start_accepting(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        text="Когда не будет?"
    )
    await state.set_state(GetData.choosing_date)


@router.message(GetData.choosing_date)
async def process_date(message: Message, state: FSMContext):
    date_text = message.text.lower()

    parsed_date = parse_date(date_text)
    print(f"Распознанная дата: {parsed_date}")

    if parsed_date == "Неправильный формат даты":
        await message.answer(
            text="Неправильный ввод даты, попробуй еще раз"
        )
        await state.set_state(GetData.choosing_date)
        return

    await state.update_data(choosing_date=parsed_date)
    await message.answer(
        text="На каких парах?(только номера)"
    )
    await state.set_state(GetData.choosing_pairs)


@router.message(GetData.choosing_pairs)
async def process_pairs(message: Message, state: FSMContext):
    pairs_text = message.text.lower()

    parsed_lessons = parse_lessons(pairs_text)

    if "Ошибка" in parsed_lessons:
        await message.answer(
            text="Неправильный ввод пар, попробуй еще раз"
        )
        print(parsed_lessons)
        await state.set_state(GetData.choosing_pairs)
        return

    print(f"Распознанные пары: {parsed_lessons}")
    await state.update_data(choosing_pairs=parsed_lessons)
    await message.answer(
        text="Причина?"
    )
    await state.set_state(GetData.choosing_reason)


@router.message(GetData.choosing_reason)
async def process_reason(message: Message, state: FSMContext):
    await state.update_data(choosing_reason=message.text.lower())
    data = await state.get_data()
    print(data)
    text = ""
    text += f'''Дата: {data['choosing_date']}
Пары: {data['choosing_pairs']}
Причина: {data['choosing_reason']}
Это правильно?'''
    await message.answer(text=text, reply_markup=is_correct_keyboard())


# Обработка правильная или неправильная информация

