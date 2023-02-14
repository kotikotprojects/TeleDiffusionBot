from bot.common import dp
from . import help_handler


def register():
    dp.register_message_handler(help_handler.help_command, commands='help')
