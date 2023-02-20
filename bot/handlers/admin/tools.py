from aiogram import types
from bot.db import db, DBTables
from bot.utils.cooldown import throttle
from bot.keyboards.exception import get_exception_keyboard
from bot.utils.trace_exception import PrettyException
from bot.modules.get_hash.get_hash import get_hash


@throttle(cooldown=5, admin_ids=db[DBTables.config].get('admins'))
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

    except Exception as e:
        exception_id = f'{message.message_thread_id}-{message.message_id}'
        db[DBTables.exceptions][exception_id] = PrettyException(e)
        await message.reply('❌ Error happened while processing your request', parse_mode='html',
                            reply_markup=get_exception_keyboard(exception_id))
        return
