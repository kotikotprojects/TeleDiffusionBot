from bot.common import dp
from bot.db.pull_db import pull


@dp.message_handler()
async def pull_db_if_new(_):
    await pull()
