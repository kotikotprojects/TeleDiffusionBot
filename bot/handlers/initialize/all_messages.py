from aiogram.types import Message
from bot.db import db, DBTables
from bot.modules.api.objects.action import Action


async def sync_db_filter(message: Message):
    from bot.db.pull_db import pull
    from bot.modules.api.ping import ping
    await pull()
    if message.is_command():
        await message.reply(f'🔄️ Bot database synchronised because of restart. '
                            f'If you tried to run a command, run it again')
    if not await ping():
        await message.reply('⚠️ Warning: StableDiffusion server is turned off or api endpoint is incorrect')


async def on_action_message(message: Message):
    action: Action = db[DBTables.actions].get(message.from_id)
    if not action:
        return
    if action.chat_id != message.chat.id:
        return
    del db[DBTables.actions][message.from_id]

    import bot.callbacks
    assert bot.callbacks
    await eval(f"bot.callbacks.{action.action_module}.{action.action}(message, '{action.overload}')")
