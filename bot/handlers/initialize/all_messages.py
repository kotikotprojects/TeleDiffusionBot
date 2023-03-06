from aiogram.types import Message


async def sync_db_filter(message: Message):
    from bot.db.pull_db import pull
    from bot.modules.api.ping import ping
    await pull()
    if message.is_command():
        await message.reply(f'🔄️ Bot database synchronised because of restart. '
                            f'If you tried to run a command, run it again')
    if not await ping():
        await message.reply('⚠️ Warning: StableDiffusion server is turned off or api endpoint is incorrect')
