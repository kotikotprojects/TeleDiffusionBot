from bot.config import BARS_APP_ID
from rich import print


async def main():
    print(BARS_APP_ID)
    import bot.handlers.register
    from bot.common import dp
    from bot.utils.commands import set_commands

    bot.handlers.register.import_handlers()
    await set_commands()
    print('[green]Bot will start now[/]')
    await dp.skip_updates()
    await dp.start_polling()


if __name__ == '__main__':
    import asyncio
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit, RuntimeError):
        print('[red]Bot stopped[/]')
