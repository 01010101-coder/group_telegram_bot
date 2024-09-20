from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.callback_data import CallbackData
from typing import Optional

from keyboards.admin_keyboards import reg_approval_keyboard
from db.users_db import UsersTable
from db.logs_db import LogsTable

from datetime import datetime

router = Router()
users_db = UsersTable()
log_db = LogsTable()


# Класс для управления callback_data
class UserApprovalCallback(CallbackData, prefix="user"):
    action: str  # "approve" или "reject"
    tg_id: Optional[int] = None


# Определение состояний
class Registration(StatesGroup):
    waiting_for_name = State()
    start_reg: Optional[str] = None


# Хэндлер для команды /start
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    user = await users_db.get_user_by_tg_id(message.from_user.id)
    await state.update_data(start_reg=datetime.now())

    if user is None:
        await message.answer("Тебя нет в базе данных, напиши свое имя и фамилию")
        await state.set_state(Registration.waiting_for_name)
    # elif user[4] == 0:
    #     await message.answer(f"Ты еще не подтвержден, сори")
    else:
        await message.answer(f"Привет, {user[1]}")


# Хэндлер для получения имени пользователя
@router.message(Registration.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    name = message.text
    tg_id = message.from_user.id
    tg_username = message.from_user.username

    # Добавляем пользователя в базу данных
    await users_db.add_user(name, tg_id, tg_username)

    start_reg = await state.get_data()
    start_reg = start_reg['start_reg']
    time_spend = (datetime.now() - start_reg).total_seconds()
    await log_db.add_log('reg', time_spend, '1')

    # Завершаем состояние FSM
    await state.clear()

    # Уведомление пользователя
    await message.answer(f"Спасибо, {name}! Ждем подтверждение.")

    # Получаем всех администраторов с рангом 3
    admins = await users_db.get_users_by_rank(3)

    # Отправляем сообщение администраторам с кнопками
    for admin in admins:
        admin_tg_id = admin[2]  # tg_id администратора
        if tg_username == "None":
            tg_username = "Не существует"
        await message.bot.send_message(
            chat_id=admin_tg_id,
            text=f"Новый пользователь {name} (@{tg_username}) ожидает подтверждения.",
            reply_markup=reg_approval_keyboard(tg_id)
        )


# Хэндлер для обработки нажатий на кнопки
@router.callback_query(UserApprovalCallback.filter())
async def callbacks_user_confirmation(callback: CallbackQuery, callback_data: UserApprovalCallback):
    if callback_data.action == "approve":
        # Обновление ранга пользователя
        await users_db.update_rank(callback_data.tg_id, 1)

        # Уведомление администратора и пользователя
        await callback.message.edit_text("Пользователь был подтвержден.")
    elif callback_data.action == "reject":
        # Удаление пользователя из базы данных
        await users_db.delete_user(callback_data.tg_id)

        # Уведомление администратора и пользователя
        await callback.message.edit_text("Пользователь был отклонен.")
        await callback.bot.send_message(chat_id=callback_data.tg_id, text="Что-то не так, тебя не подтвердили(")
