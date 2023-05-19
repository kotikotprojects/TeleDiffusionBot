from aiogram import types
from bot.db import db, DBTables
from bot.utils.cooldown import throttle
from bot.keyboards.image_info import get_img_info_keyboard
from bot.utils.errorable_command import wrap_exception


@wrap_exception([IndexError])
@throttle(cooldown=10, admin_ids=db[DBTables.config].get('admins', []))
async def imginfo(message: types.Message):
    try:
        if not hasattr(message.reply_to_message, 'photo'):
            await message.reply('❌ Reply with this command on picture', parse_mode='html')
            return

        if not db[DBTables.generated].get(message.reply_to_message.photo[0].file_unique_id):
            await message.reply('❌ This picture wasn\'t generated using this bot '
                                'or doesn\'t exist in database. Note this only works on '
                                'files forwarded from bot.', parse_mode='html')
            return

        await message.reply("Image was generated using this bot", reply_markup=get_img_info_keyboard(
            message.reply_to_message.photo[0].file_unique_id
        ))

    except IndexError:
        await message.reply('❌ Reply with this command on PICTURE', parse_mode='html')
