from aiogram import Router, types, F
from keyboards.general_keyboards import main_menu_keyboard


router = Router()


@router.message()
async def process_function(message: types.Message):
    await message.answer("Что надо?", reply_markup=main_menu_keyboard())
