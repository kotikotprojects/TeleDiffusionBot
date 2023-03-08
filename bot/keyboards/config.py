from aiogram import types
from bot.db import db, DBTables
from bot.callbacks.factories.config import (prompt_settings_data, global_settings_data, admin_settings_data)
from bot.callbacks.factories.common import close_keyboard_data


def get_config_keyboard(user_id: int) -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton("Prompt settings", callback_data=prompt_settings_data.new()),
        types.InlineKeyboardButton("Global settings", callback_data=global_settings_data.new())
    ]
    if user_id in db[DBTables.config].get('admins'):
        buttons.append(
            types.InlineKeyboardButton("Admin settings", callback_data=admin_settings_data.new())
        )

    buttons.append(
        types.InlineKeyboardButton("🔻 Close", callback_data=close_keyboard_data.new())
    )
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard
