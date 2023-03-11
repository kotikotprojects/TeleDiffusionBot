from bot.common import dp
from bot.keyboards.config import get_config_keyboard
from bot.utils.private_keyboard import other_user
from aiogram import types, filters
from .prompt_settings import register
from .global_settings import register
from .admin_settings import register


async def back_to_config(call: types.CallbackQuery):
    if await other_user(call):
        return

    await call.message.edit_text("⚙️ Configuration:")
    await call.message.edit_reply_markup(get_config_keyboard(call.from_user.id))


def register():
    prompt_settings.register()
    global_settings.register()
    admin_settings.register()
    dp.register_callback_query_handler(back_to_config, filters.Text('config_back'))
