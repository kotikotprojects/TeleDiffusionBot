from aiogram import types
from bot.db import db, DBTables
from bot.callbacks.factories.config import prompt_settings_data, admin_settings_data


def get_config_keyboard(user_id: int) -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton("Prompt settings", callback_data="prompt_settings_kb"),
        types.InlineKeyboardButton("Global settings", callback_data="global_settings_kb")
    ]
    if user_id in db[DBTables.config].get('admins', []):
        buttons.append(
            types.InlineKeyboardButton("Admin settings", callback_data="admin_settings_kb")
        )

    buttons.append(
        types.InlineKeyboardButton("🔻 Close", callback_data="close_keyboard")
    )
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def get_prompt_settings_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton("Prompt", callback_data=prompt_settings_data.new("prompt")),
        types.InlineKeyboardButton("Negative prompt", callback_data=prompt_settings_data.new("negative_prompt")),
        types.InlineKeyboardButton("Steps count", callback_data=prompt_settings_data.new("steps")),
        types.InlineKeyboardButton("CFG Scale (model creativity)", callback_data=prompt_settings_data.new("cfg_scale")),
        types.InlineKeyboardButton("Size", callback_data=prompt_settings_data.new("size")),
        types.InlineKeyboardButton("Restore faces", callback_data=prompt_settings_data.new("restore_faces")),
        types.InlineKeyboardButton("Sampler", callback_data=prompt_settings_data.new("sampler")),
        types.InlineKeyboardButton("👈 Back", callback_data="config_back"),
        types.InlineKeyboardButton("🔻 Close", callback_data="close_keyboard")
    ]

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def get_global_settings_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton("Set model", callback_data="global_settings_set_model"),
        types.InlineKeyboardButton("👈 Back", callback_data="config_back"),
        types.InlineKeyboardButton("🔻 Close", callback_data="close_keyboard")
    ]

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def get_admin_settings_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton("Add admin", callback_data=admin_settings_data.new("aliases.add_admin")),
        types.InlineKeyboardButton("Remove admin", callback_data=admin_settings_data.new("aliases.remove_admin")),
        types.InlineKeyboardButton("Set API endpoint", callback_data=admin_settings_data.new("aliases.set_endpoint")),
        types.InlineKeyboardButton("Reset generation queue", callback_data=admin_settings_data.new("reset.resetqueue")),
        types.InlineKeyboardButton("Turn on/off generation",
                                   callback_data=admin_settings_data.new("on_off.on_off_call")),
        types.InlineKeyboardButton("👈 Back", callback_data="config_back"),
        types.InlineKeyboardButton("🔻 Close", callback_data="close_keyboard")
    ]

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard
