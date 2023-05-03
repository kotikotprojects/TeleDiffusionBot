from aiogram import types
from bot.db import db, DBTables, decrypt
from bot.utils.cooldown import throttle
from bot.keyboards.set_model import get_set_model_keyboard
from bot.modules.api.models import get_models
from bot.utils.errorable_command import wrap_exception


@wrap_exception()
@throttle(cooldown=30*60, admin_ids=db[DBTables.config].get('admins'), by_id=False)
async def set_model_command(message: types.Message):
    models = await get_models()
    if models is not None and len(models) > 0:
        db[DBTables.config]['models'] = models
    else:
        await message.reply('❌ No models available')
        return

    await message.reply("🪄 You can choose model from available:", reply_markup=get_set_model_keyboard(0))
