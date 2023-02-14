from rich import print
from aiogram.types import BotCommand
from bot.common import bot


async def set_commands():
    from bot.handlers.help_command.help_strings import help_data

    await bot.set_my_commands(
        commands=list(
            map(
                (lambda x: BotCommand(
                    command='/' + x,
                    description=help_data.get(x) if help_data.get(x) else f'No info for {x}'
                )
                 ), help_data.keys())
        ) + [BotCommand(command='/help', description='Get commands list or info by command')]
    )

    print('[gray]Commands registered[/]')
