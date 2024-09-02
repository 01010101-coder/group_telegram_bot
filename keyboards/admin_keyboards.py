from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def approval_keyboard(tg_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅",
                    callback_data=f"user:approve:{tg_id}"
                ),
                InlineKeyboardButton(
                    text="🚫",
                    callback_data=f"user:reject:{tg_id}"
                ),
            ]
        ]
    )
