from bot.common import dp
from .aliases import *


def register():
    dp.register_message_handler(set_endpoint, commands='setendpoint')
