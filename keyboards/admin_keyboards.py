from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def reg_approval_keyboard(tg_id: int) -> InlineKeyboardMarkup:
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


def skip_approval_keyboard(tg_id: int, date: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅",
                    callback_data=f"skip:approve:{tg_id}:{date}"
                ),
                InlineKeyboardButton(
                    text="🚫",
                    callback_data=f"skip:reject:{tg_id}:{date}"
                ),
            ]
        ]
    )
