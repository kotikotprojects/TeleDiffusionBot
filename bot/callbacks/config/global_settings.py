from bot.common import dp
from bot.utils.private_keyboard import other_user
from bot.db import db, DBTables
from aiogram import types, filters
from bot.utils.errorable_command import wrap_exception
from bot.utils.cooldown import throttle


async def on_global_settings_kb_open(call: types.CallbackQuery):
    from bot.keyboards.config import get_global_settings_keyboard
    if await other_user(call):
        return

    await call.message.edit_text("⚙️ Global configuration", reply_markup=get_global_settings_keyboard())


@wrap_exception()
@throttle(cooldown=60*60, admin_ids=db[DBTables.config].get('admins', []), by_id=False)
async def on_set_model(call: types.CallbackQuery):
    from bot.keyboards.set_model import get_set_model_keyboard
    from bot.modules.api.models import get_models

    if await other_user(call):
        return

    models = await get_models()
    if models is not None and len(models) > 0:
        db[DBTables.config]['models'] = models
    else:
        await call.answer('❌ No models available', show_alert=True)
        return

    await call.message.edit_text("🪄 You can choose model from available:",
                                 reply_markup=get_set_model_keyboard(0).add(
                                     types.InlineKeyboardButton("👈 Back", callback_data="global_settings_kb")
                                 ))


def register():
    dp.register_callback_query_handler(on_set_model, filters.Text("global_settings_set_model"))
    dp.register_callback_query_handler(on_global_settings_kb_open, filters.Text("global_settings_kb"))
