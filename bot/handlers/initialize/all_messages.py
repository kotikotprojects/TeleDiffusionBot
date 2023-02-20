from aiogram.types import Message
from bot.db.pull_db import pull


async def sync_db_filter(message: Message):
    await pull()
    if message.is_command():
        await message.reply(f'🔄️ Bot database synchronised because of restart. '
                            f'If you tried to run a command, run it again')
