from bot.common import dp
from ..factories import config as config_factory
from bot.utils.private_keyboard import other_user
from bot.modules.api.objects.action import Action
from bot.db import db, DBTables
from aiogram import types, filters


async def on_prompt_settings_kb_open(call: types.CallbackQuery):
    from bot.keyboards.config import get_prompt_settings_keyboard
    if await other_user(call):
        return

    await call.message.edit_text("⚙️ Prompt configuration", reply_markup=get_prompt_settings_keyboard())


async def on_prompt_settings_set(call: types.CallbackQuery, callback_data: dict):
    overload = callback_data['setting']
    if await other_user(call):
        return

    db[DBTables.actions][call.from_user.id] = Action(
        chat_id=call.message.chat.id,
        action_module='config.prompt_settings',
        action='on_prompt_settings_action',
        overload=overload
    )

    await call.message.edit_text(
        f"⚒️ Type new {overload} value in this chat: ",
        reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(
            "👈 Back",
            callback_data="prompt_settings_kb")
        )
    )


async def on_prompt_settings_action(message: types.Message, overload):
    assert message
    from bot.handlers.txt2img import set_settings
    assert set_settings
    await eval(f"set_settings.set_{overload}_command(message, is_command=False)")


def register():
    dp.register_callback_query_handler(on_prompt_settings_set, config_factory.prompt_settings_data.filter())
    dp.register_callback_query_handler(on_prompt_settings_kb_open, filters.Text("prompt_settings_kb"))
