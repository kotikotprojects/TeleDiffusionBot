from aiogram import types
from bot.db import db, DBTables, encrypt
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

    db[DBTables.config]['endpoint'] = encrypt(message.get_args())

    await db[DBTables.config].write()

    await message.reply("✅ New url set")


@throttle(5)
async def add_admin(message: types.Message):
    if message.from_id != ADMIN:
        await message.reply('❌ You are not permitted to do that. It is only for main admin')
        return

    if not message.get_args().isdecimal() and not hasattr(message.reply_to_message, 'text'):
        await message.reply('❌ Put new admin ID to command arguments or answer to users message')
        return
    elif not message.get_args().isdecimal():
        ID = message.reply_to_message.from_id
    elif not hasattr(message.reply_to_message, 'text'):
        ID = int(message.get_args())

    if not isinstance(db[DBTables.config].get('admins'), list):
        db[DBTables.config]['admins'] = list()

    if ID not in db[DBTables.config].get('admins'):
        admins_ = db[DBTables.config].get('admins')
        admins_.append(ID)
        db[DBTables.config]['admins'] = admins_
    else:
        await message.reply('❌ This admin is added already')
        return

    await db[DBTables.config].write()

    await message.reply("✅ Added admin")


@throttle(5)
async def remove_admin(message: types.Message):
    if message.from_id != ADMIN:
        await message.reply('❌ You are not permitted to do that. It is only for main admin')
        return

    if not message.get_args().isdecimal() and not hasattr(message.reply_to_message, 'text'):
        await message.reply('❌ Put admin ID to command arguments or answer to users message')
        return
    elif not message.get_args().isdecimal():
        ID = message.reply_to_message.from_id
    elif not hasattr(message.reply_to_message, 'text'):
        ID = int(message.get_args())

    if not isinstance(db[DBTables.config].get('admins'), list):
        db[DBTables.config]['admins'] = list()

    if ID not in db[DBTables.config].get('admins'):
        await message.reply('❌ This admin is not added')
        return
    else:
        admins_ = db[DBTables.config].get('admins')
        admins_.remove(ID)
        db[DBTables.config]['admins'] = admins_

    await db[DBTables.config].write()

    await message.reply("✅ Removed admin")
