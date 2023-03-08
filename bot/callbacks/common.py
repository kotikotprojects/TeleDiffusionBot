from bot.common import dp
from bot.callbacks.factories.common import close_keyboard_data
from aiogram import types
from bot.utils.private_keyboard import other_user


async def on_close_keyboard(call: types.CallbackQuery):
    if await other_user(call):
        return

    await call.message.delete()


def register():
    dp.register_callback_query_handler(on_close_keyboard, close_keyboard_data.filter())
