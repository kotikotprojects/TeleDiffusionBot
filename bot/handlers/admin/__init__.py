from bot.common import dp
from .aliases import *
from .reset import *


def register():
    dp.register_message_handler(set_endpoint, commands='setendpoint')
    dp.register_message_handler(reset.resetqueue, commands='resetqueue')
