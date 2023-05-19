from aiogram import types
from bot.db import db, DBTables
from bot.config import ADMIN
from bot.utils.cooldown import throttle


@throttle(5)
async def resetqueue(message: types.Message, is_command: bool = True):
    if message.from_id not in db[DBTables.config].get('admins', []) and message.from_id != ADMIN:
        await message.reply('❌ You are not permitted to do that. '
                            'It is only for this bot instance maintainers and admins')
        return

    if not is_command and message.text.lower() != 'reset':
        return

    db[DBTables.queue]['n'] = 0

    await db[DBTables.config].write()

    await message.reply("✅ Reset queue")
