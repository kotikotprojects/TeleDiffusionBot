from aiogram import types
from bot.db import db, DBTables
from bot.callbacks.factories.set_model import set_model_page, set_model


def get_set_model_keyboard(page: int) -> types.InlineKeyboardMarkup:
    models = db[DBTables.config]['models']
    navigation_buttons = list()
    page = int(page)

    if page > 0:
        navigation_buttons.append(types.InlineKeyboardButton(
            '<',
            callback_data=set_model_page.new(page=page - 1)
        ))
    if len([models[i:i + 5] for i in range(0, len(models), 5)]) > page + 1:
        navigation_buttons.append(types.InlineKeyboardButton(
            '>',
            callback_data=set_model_page.new(page=page + 1)
        ))

    models_buttons = [types.InlineKeyboardButton(models[i], callback_data=set_model.new(i)) for i in range(len(models))]

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    if len(models) > 5:
        keyboard.add(*[models_buttons[i:i + 5] for i in range(0, len(models_buttons), 5)][page])
        keyboard.row(*navigation_buttons)
    else:
        keyboard.add(*models_buttons)

    keyboard.add(
        types.InlineKeyboardButton("🔻 Cancel", callback_data="close_keyboard")
    )

    return keyboard
