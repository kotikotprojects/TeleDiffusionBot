from bot.common import dp
from bot.db import db, DBTables
from aiogram import types
from .factories.set_model import set_model, set_model_page
from bot.keyboards.set_model import get_set_model_keyboard
from bot.utils.private_keyboard import other_user
from bot.modules.api import models
from bot.utils.errorable_command import wrap_exception


@wrap_exception()
async def on_set_model(call: types.CallbackQuery, callback_data: dict):
    n = int(callback_data['n'])
    await call.message.edit_reply_markup(reply_markup=None)
    await models.set_model(db[DBTables.config]['models'][n])

    await call.message.answer('✅ Model set for all users!')
    await call.message.delete()


async def on_page_change(call: types.CallbackQuery, callback_data: dict):
    page = callback_data['page']
    if await other_user(call):
        return

    await call.message.edit_reply_markup(
        get_set_model_keyboard(page)
    )


def register():
    dp.register_callback_query_handler(on_set_model, set_model.filter())
    dp.register_callback_query_handler(on_page_change, set_model_page.filter())
