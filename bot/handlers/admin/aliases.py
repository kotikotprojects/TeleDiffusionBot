from aiogram import types
from bot.db import db, DBTables, encrypt
import validators
from bot.config import ADMIN
from bot.utils.cooldown import throttle


@throttle(5)
async def set_endpoint(message: types.Message, is_command: bool = True):
    if message.from_id not in db[DBTables.config].get('admins', []) and message.from_id != ADMIN:
        await message.reply('❌ You are not permitted to do that. '
                            'It is only for this bot instance maintainers and admins')
        return

    if not (message.get_args() if is_command else message.text) or not \
            validators.url((message.get_args() if is_command else message.text)):
        await message.reply("❌ Specify correct url for endpoint")
        return

    db[DBTables.config]['endpoint'] = encrypt((message.get_args() if is_command else message.text))

    await db[DBTables.config].write()

    await message.reply("✅ New url set")


@throttle(5)
async def add_whitelist(message: types.Message, is_command: bool = True):
    if message.from_id != ADMIN:
        await message.reply('❌ You are not permitted to do that. It is only for main admin')
        return

    if not (message.get_args() if is_command else message.text).isdecimal() and not \
            hasattr(message.reply_to_message, 'text') and (message.chat.id >= 0):
        await message.reply('❌ Put new whitelist chat ID to command arguments')
        return
    elif not (message.get_args() if is_command else message.text).isdecimal() and not \
            hasattr(message.reply_to_message, 'text') and (message.chat.id < 0):
        ID = message.chat.id
        await message.reply(f'Chat ID: {message.chat.id} Chat title: {message.chat.title}')
    elif not (message.get_args() if is_command else message.text).isdecimal():
        ID = message.reply_to_message.from_id
    elif not hasattr(message.reply_to_message, 'text'):
        ID = int((message.get_args() if is_command else message.text))

    if not isinstance(db[DBTables.config].get('whitelist'), list):
        db[DBTables.config]['whitelist'] = list()

    if ID not in db[DBTables.config].get('whitelist', []):
        whitelist_ = db[DBTables.config].get('whitelist', [])
        whitelist_.append(ID)
        db[DBTables.config]['whitelist'] = whitelist_
    else:
        await message.reply('❌ This whitelist is added already')
        return

    await db[DBTables.config].write()

    await message.reply("✅ Added whitelist")


@throttle(5)
async def remove_whitelist(message: types.Message, is_command: bool = True):
    if message.from_id != ADMIN:
        await message.reply('❌ You are not permitted to do that. It is only for main admin')
        return

    if not (message.get_args() if is_command else message.text).isdecimal() and not \
            hasattr(message.reply_to_message, 'text') and (message.chat.id) >= 0:
        await message.reply('❌ Put whitelist ID to command arguments or answer to users message')
        return
    elif not (message.get_args() if is_command else message.text).isdecimal() and not \
            hasattr(message.reply_to_message, 'text') and (message.chat.id < 0):
        ID = message.chat.id
        await message.reply(f'Chat ID: {message.chat.id} Chat title: {message.chat.title}')
    elif not (message.get_args() if is_command else message.text).isdecimal():
        ID = message.reply_to_message.from_id
    elif not hasattr(message.reply_to_message, 'text'):
        ID = int((message.get_args() if is_command else message.text))

    if not isinstance(db[DBTables.config].get('whitelist'), list):
        db[DBTables.config]['whitelist'] = list()

    if ID not in db[DBTables.config].get('whitelist', []):
        await message.reply('❌ This whitelist is not added')
        return
    else:
        whitelist_ = db[DBTables.config].get('whitelist', [])
        whitelist_.remove(ID)
        db[DBTables.config]['whitelist'] = whitelist_

    await db[DBTables.config].write()

    await message.reply("✅ Removed whitelist")


@throttle(5)
async def get_whitelist(message: types.Message, is_command: bool = True):
    if message.from_id != ADMIN:
        await message.reply('❌ You are not permitted to do that. It is only for main admin')
        return

    await message.reply(f"✅ Whitelisted ids: {db[DBTables.config].get('whitelist')}"
                        if db[DBTables.config].get('whitelist', []) else
                        '❌ Whitelist is disabled. Everyone can use the bot. Add someone to whitelist to enable it')


@throttle(5)
async def add_admin(message: types.Message, is_command: bool = True):
    if message.from_id != ADMIN:
        await message.reply('❌ You are not permitted to do that. It is only for main admin')
        return

    if not (message.get_args() if is_command else message.text).isdecimal() and not \
            hasattr(message.reply_to_message, 'text'):
        await message.reply('❌ Put new admin ID to command arguments or answer to users message')
        return
    elif not (message.get_args() if is_command else message.text).isdecimal():
        ID = message.reply_to_message.from_id
    elif not hasattr(message.reply_to_message, 'text'):
        ID = int((message.get_args() if is_command else message.text))

    if not isinstance(db[DBTables.config].get('admins'), list):
        db[DBTables.config]['admins'] = list()

    if ID not in db[DBTables.config].get('admins', []):
        admins_ = db[DBTables.config].get('admins', [])
        admins_.append(ID)
        db[DBTables.config]['admins'] = admins_
    else:
        await message.reply('❌ This admin is added already')
        return

    await db[DBTables.config].write()

    await message.reply("✅ Added admin")


@throttle(5)
async def remove_admin(message: types.Message, is_command: bool = True):
    if message.from_id != ADMIN:
        await message.reply('❌ You are not permitted to do that. It is only for main admin')
        return

    if not (message.get_args() if is_command else message.text).isdecimal() and not \
            hasattr(message.reply_to_message, 'text'):
        await message.reply('❌ Put admin ID to command arguments or answer to users message')
        return
    elif not (message.get_args() if is_command else message.text).isdecimal():
        ID = message.reply_to_message.from_id
    elif not hasattr(message.reply_to_message, 'text'):
        ID = int((message.get_args() if is_command else message.text))

    if not isinstance(db[DBTables.config].get('admins'), list):
        db[DBTables.config]['admins'] = list()

    if ID not in db[DBTables.config].get('admins', []):
        await message.reply('❌ This admin is not added')
        return
    else:
        admins_ = db[DBTables.config].get('admins', [])
        admins_.remove(ID)
        db[DBTables.config]['admins'] = admins_

    await db[DBTables.config].write()

    await message.reply("✅ Removed admin")
