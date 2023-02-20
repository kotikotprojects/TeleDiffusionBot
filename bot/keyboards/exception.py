from aiogram import types
from bot.callbacks.factories.exception import exception_callback


def get_exception_keyboard(e_id: str) -> types.InlineKeyboardMarkup:
    buttons = [types.InlineKeyboardButton(text="Show full stack", callback_data=exception_callback.new(e_id=e_id))]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard
