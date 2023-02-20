from bot.common import dp
from .aliases import *
from .reset import *
from .tools import *


def register():
    dp.register_message_handler(set_endpoint, commands='setendpoint')
    dp.register_message_handler(reset.resetqueue, commands='resetqueue')
    dp.register_message_handler(tools.hash_command, commands='hash')
