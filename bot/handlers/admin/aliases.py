from aiogram import types
from bot.db import db, DBTables
import validators
from bot.config import ADMIN
from bot.utils.cooldown import throttle


@throttle(5)
async def set_endpoint(message: types.Message):
    if message.from_id not in db[DBTables.config].get('admins') and message.from_id != ADMIN:
        await message.reply('❌ You are not permitted to do that. '
                            'It is only for this bot instance maintainers and admins')
        return

    if not message.get_args() or not validators.url(message.get_args()):
        await message.reply("❌ Specify correct url for endpoint")
        return

    db[DBTables.config]['endpoint'] = message.get_args()

    await db[DBTables.config].write()

    await message.reply("✅ New url set")
