from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData


choice = ReplyKeyboardMarkup(one_time_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                "🕒 Создать событие 🕒"
            )
        ],
        [
            KeyboardButton(
                "🔕 Удалить событие 🔕"
            ),
            KeyboardButton(
                "🔔 Мои события 🔔"
            )
        ],
        [
            KeyboardButton(
                "🚫 Удалить все события 🚫"
            )
        ]
    ]
)

