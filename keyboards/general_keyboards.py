from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Нет на паре", callback_data="net_na_pare")
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


def choose_enter_method() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Вручную", callback_data="manually_enter")
            ],
            [
                InlineKeyboardButton(text="Через нейросеть(BETA)", callback_data="gpt_enter")
            ]
        ]
    )