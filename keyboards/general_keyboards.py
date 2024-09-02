from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Нет на паре", callback_data="net_na_pare"),
                InlineKeyboardButton(text="Функция 2", callback_data="function_2"),
            ],
            [
                InlineKeyboardButton(text="Функция 3", callback_data="function_3"),
                InlineKeyboardButton(text="Функция 4", callback_data="function_4"),
            ]
        ]
    )


def update_state_keyboard(prev_action) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Назад", callback_data=f"back_to_{prev_action}"),
                InlineKeyboardButton(text="Отмена", callback_data="cancel")
            ]
        ]
    )
