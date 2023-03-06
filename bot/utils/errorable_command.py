from functools import wraps
from bot.db import db, DBTables
from bot.keyboards.exception import get_exception_keyboard
from bot.utils.trace_exception import PrettyException
from aiohttp import ClientConnectorError
from aiogram import types


def wrap_exception(unhandled_types: list = None, custom_loading: bool = False):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            message = args[0]
            if not custom_loading:
                if isinstance(message, types.Message):
                    temp_message = await message.reply('⏳ Loading...')
                elif isinstance(message, types.CallbackQuery):
                    temp_message = await message.message.answer('⏳ Loading...')
                else:
                    raise AttributeError("This wrapper is only for commands!")
            try:
                _ = await func(*args, **kwargs)
                if not custom_loading:
                    await temp_message.delete()
                return _

            except ClientConnectorError:
                r_string = '❌ Error! Maybe, StableDiffusion API endpoint is incorrect ' \
                           'or turned off'
                if isinstance(message, types.Message):
                    await message.reply(r_string)
                elif isinstance(message, types.CallbackQuery):
                    await message.message.answer(r_string)

                if not custom_loading:
                    await temp_message.delete()
                return

            except Exception as e:
                if not unhandled_types or e.__class__ not in unhandled_types:
                    exception_id = f'{message.message_thread_id}-{message.message_id}'
                    db[DBTables.exceptions][exception_id] = PrettyException(e)
                    if not custom_loading:
                        await temp_message.delete()
                    if isinstance(message, types.Message):
                        await message.reply('❌ Error happened while processing your request', parse_mode='html',
                                            reply_markup=get_exception_keyboard(exception_id))
                    elif isinstance(message, types.CallbackQuery):
                        await message.message.reply('❌ Error happened while processing your request',
                                                    parse_mode='html',
                                                    reply_markup=get_exception_keyboard(exception_id))
                    return
                else:
                    raise e

        return wrapper

    return decorator
