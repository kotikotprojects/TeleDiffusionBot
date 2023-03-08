from bot.common import dp
from .config_command import *


def register():
    dp.register_message_handler(config_command, commands='config')
