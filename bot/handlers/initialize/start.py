from aiogram import types
from bot.db import db, DBTables
from bot.config import ADMIN
from bot.utils.cooldown import throttle


@throttle(10)
async def start_command(message: types.Message):
    if message.from_id == ADMIN:
        await message.reply(f'👋 Hello, {message.from_user.username}. You are admin of this instance, '
                            f'so we will check config for you now')
        if not isinstance(db[DBTables.config].get('admins'), list):
            db[DBTables.config]['admins'] = list()
        if ADMIN not in db[DBTables.config].get('admins', []):
            admins_ = db[DBTables.config].get('admins', [])
            admins_.append(ADMIN)
            db[DBTables.config]['admins'] = admins_
            await db[DBTables.config].write()
            await message.reply(f'✅ Added {message.from_user.username} to admins. You can add other admins, '
                                f'check bot settings menu')
        if db[DBTables.config].get('enabled') is None:
            db[DBTables.config]['enabled'] = True
            await message.reply(f'✅ Generation is enabled now')
        return

    await message.reply(f'👋 Hello, {message.from_user.username}. Use /help to see available commands.')
