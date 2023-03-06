from aiogram import types
from bot.db import db, DBTables
from bot.utils.cooldown import throttle
from bot.modules.api.ping import ping


@throttle(cooldown=5, admin_ids=db[DBTables.config].get('admins'))
async def get_status(message: types.Message):
    temp_message = await message.reply('⏳ Sending request...')
    try:
        if await ping():
            await message.reply('💚 Endpoint is UP')
        else:
            raise Exception

    except Exception as e:
        assert e
        await message.reply('💔 Endpoint is probably DOWN or incorrect')

    await temp_message.delete()
