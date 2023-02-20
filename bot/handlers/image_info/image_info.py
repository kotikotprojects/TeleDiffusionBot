from aiogram import types
from bot.db import db, DBTables
from bot.utils.cooldown import throttle
from bot.keyboards.exception import get_exception_keyboard
from bot.utils.trace_exception import PrettyException


@throttle(cooldown=10, admin_ids=db[DBTables.config].get('admins'))
async def imginfo(message: types.Message):
    try:
        if not hasattr(message.reply_to_message, 'photo'):
            await message.reply('❌ Reply with this command on picture', parse_mode='html')
            return

        if not (original_r := db[DBTables.generated].get(message.reply_to_message.photo[0].file_unique_id)):
            await message.reply('❌ This picture wasn\'t generated using this bot '
                                'or doesn\'t exist in database. Note this only works on '
                                'files forwarded from bot.', parse_mode='html')
            return

        await message.reply(str(original_r))

    except IndexError:
        await message.reply('❌ Reply with this command on PICTURE', parse_mode='html')

    except Exception as e:
        exception_id = f'{message.message_thread_id}-{message.message_id}'
        db[DBTables.exceptions][exception_id] = PrettyException(e)
        await message.reply('❌ Error happened while processing your request', parse_mode='html',
                            reply_markup=get_exception_keyboard(exception_id))
        return
