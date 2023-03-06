from bot.common import dp
from bot.db import db, DBTables
from aiogram import types
from .factories.set_model import set_model, set_model_page
from bot.keyboards.set_model import get_set_model_keyboard
from bot.utils.private_keyboard import other_user
from bot.keyboards.exception import get_exception_keyboard
from bot.utils.trace_exception import PrettyException
from aiohttp import ClientConnectorError
from bot.modules.api import models


async def on_set_model(call: types.CallbackQuery, callback_data: dict):
    n = int(callback_data['n'])
    temp_message = await call.message.answer('⏳ Setting model...')
    try:
        await models.set_model(db[DBTables.config]['models'][n])

    except ClientConnectorError:
        await call.answer('❌ Error! Maybe, StableDiffusion API endpoint is incorrect '
                          'or turned off', show_alert=True)
        await call.message.delete()
        await temp_message.delete()
        return

    except Exception as e:
        exception_id = f'{call.message.message_thread_id}-{call.message.message_id}'
        db[DBTables.exceptions][exception_id] = PrettyException(e)
        await call.message.reply('❌ Error happened while processing your request', parse_mode='html',
                                 reply_markup=get_exception_keyboard(exception_id))
        db[DBTables.queue]['n'] = db[DBTables.queue].get('n', 1) - 1
        return

    await temp_message.answer('✅ Model set for all users!')
    await temp_message.delete()


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
