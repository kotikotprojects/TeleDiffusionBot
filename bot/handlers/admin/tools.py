from aiogram import types
from bot.db import db, DBTables
from bot.utils.cooldown import throttle
from bot.utils.errorable_command import wrap_exception
from bot.modules.get_hash.get_hash import get_hash


@wrap_exception([IndexError])
@throttle(cooldown=5, admin_ids=db[DBTables.config].get('admins', []))
async def hash_command(message: types.Message):
    try:
        if not hasattr(message.reply_to_message, 'photo') or not hasattr(message.reply_to_message, 'document'):
            await message.reply('❌ REPLY with this command on picture or file', parse_mode='html')
            return

        if len(message.reply_to_message.photo) < 1:
            file_hash = await get_hash(message.reply_to_message.document.file_id)

        else:
            file_hash = await get_hash(message.reply_to_message.photo[0].file_id)

        await message.reply((lambda x: x if x else "❌ Hash not returned")(file_hash))

    except IndexError:
        await message.reply('❌ Reply with this command on PICTURE OR FILE', parse_mode='html')
