from aiogram.types import Message
from bot.db.pull_db import pull


async def sync_db_filter(message: Message):
    await pull()
    await message.reply(f'🔄️ Bot database synchronised. If you tried to run a command, run it again')
