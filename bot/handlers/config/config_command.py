from aiogram import types
from bot.db import db, DBTables
from bot.utils.cooldown import throttle
from bot.utils.errorable_command import wrap_exception
from bot.keyboards.config import get_config_keyboard


@wrap_exception()
@throttle(cooldown=20, admin_ids=db[DBTables.config].get('admins', []), by_id=False)
async def config_command(message: types.Message):
    await message.reply("⚙️ Configuration:", reply_markup=get_config_keyboard(message.from_id))
