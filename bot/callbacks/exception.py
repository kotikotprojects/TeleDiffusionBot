from bot.common import dp
from bot.db import db, DBTables
from aiogram import types
from .factories.exception import exception_callback


async def on_exception(call: types.CallbackQuery, callback_data: dict):
    e_id = callback_data['e_id']
    e = db[DBTables.exceptions][e_id]
    del db[DBTables.exceptions][e_id]
    await call.message.edit_text(e, parse_mode='html')


def register():
    dp.register_callback_query_handler(on_exception, exception_callback.filter())
