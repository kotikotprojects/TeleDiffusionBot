from bot.common import dp
from ..factories import config as config_factory
from bot.utils.private_keyboard import other_user
from bot.modules.api.objects.action import Action
from bot.db import db, DBTables
from aiogram import types, filters


async def on_admin_settings_kb_open(call: types.CallbackQuery):
    from bot.keyboards.config import get_admin_settings_keyboard
    if await other_user(call):
        return

    await call.message.edit_text("⚙️ Administrative configuration", reply_markup=get_admin_settings_keyboard())


async def on_admin_settings_set(call: types.CallbackQuery, callback_data: dict):
    overload = callback_data['setting']
    if await other_user(call):
        return

    db[DBTables.actions][call.from_user.id] = Action(
        chat_id=call.message.chat.id,
        action_module='config.admin_settings',
        action='on_admin_settings_action',
        overload=overload
    )

    await call.message.edit_text(
        f"⚒️ Type id or answer to message of this user to {'add' if 'add' in overload else 'remove'} admin: "
        if 'aliases' in overload and 'admin' in overload and ('add' in overload or 'remove' in overload)
        else f"⚒️ Type new endpoint address: " if "aliases.set_endpoint" in overload
        else f"⚒️ Type \"reset\" if you REALLY want to reset queue: " if "reset.resetqueue" in overload
        else f"⚒️ Type \"on\" or \"off\" to change generation mode: " if "on_off" in overload
        else f"❌ Not found...",
        reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(
            "👈 Back",
            callback_data="admin_settings_kb")
        )
    )


async def on_admin_settings_action(message: types.Message, overload):
    assert message
    from bot.handlers import admin
    assert admin
    await eval(f"admin.{overload}(message, is_command=False)")


def register():
    dp.register_callback_query_handler(on_admin_settings_set, config_factory.admin_settings_data.filter())
    dp.register_callback_query_handler(on_admin_settings_kb_open, filters.Text("admin_settings_kb"))
