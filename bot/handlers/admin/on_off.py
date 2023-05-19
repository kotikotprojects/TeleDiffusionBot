from aiogram import types
from bot.db import db, DBTables
from bot.config import ADMIN
from bot.utils.cooldown import throttle


@throttle(5)
async def on_off_call(message: types.Message, is_command=None):
    if message.from_id not in db[DBTables.config].get('admins', []) and message.from_id != ADMIN:
        await message.reply('❌ You are not permitted to do that. '
                            'It is only for this bot instance maintainers and admins')
        return

    db[DBTables.config]['enabled'] = False if message.text.lower() == 'off' else True
    await db[DBTables.config].write()

    await message.reply(f"Generation enabled: {'💚 (yes)' if db[DBTables.config].get('enabled') else '💔 (no)'}")
