from aiogram import types
from .help_strings import help_data


async def help_command(message: types.Message):
    if message.get_args() == "":
        await message.reply(
            "\n".join(
                list(
                    map(
                        (lambda x: f"/{x} - {help_data.get(x) if help_data.get(x) else f'No info for {x}'}"),
                        help_data.keys()
                    )
                )
            )
        )
    else:
        if help_data.get(message.get_args()):
            await message.reply(help_data.get(message.get_args()))
        else:
            await message.reply(f"No info for {message.get_args()}")
