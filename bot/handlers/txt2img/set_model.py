from aiogram import types
from bot.db import db, DBTables
from bot.utils.cooldown import throttle
from bot.keyboards.set_model import get_set_model_keyboard
from bot.keyboards.exception import get_exception_keyboard
from bot.utils.trace_exception import PrettyException
from bot.modules.api.models import get_models
from aiohttp import ClientConnectorError


@throttle(cooldown=60*60, admin_ids=db[DBTables.config].get('admins'), by_id=False)
async def set_model_command(message: types.Message):
    temp_message = await message.reply('⏳ Getting models...')
    try:
        models = await get_models()
        if models is not None and len(models) > 0:
            db[DBTables.config]['models'] = models
        else:
            await temp_message.delete()
            await message.reply('❌ No models available')
            return

        await temp_message.delete()
        await message.reply("🪄 You can choose model from available:", reply_markup=get_set_model_keyboard(0))

    except ClientConnectorError:
        await message.reply('❌ Error! Maybe, StableDiffusion API endpoint is incorrect '
                            'or turned off')
        await temp_message.delete()
        return

    except Exception as e:
        exception_id = f'{message.message_thread_id}-{message.message_id}'
        db[DBTables.exceptions][exception_id] = PrettyException(e)
        await message.reply('❌ Error happened while processing your request', parse_mode='html',
                            reply_markup=get_exception_keyboard(exception_id))
        return
