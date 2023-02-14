from bot.common import dp, bot
from .start import *
from .all_messages import *


def register():
    dp.register_message_handler(all_messages.sync_db_filter, lambda *_: not hasattr(bot, 'cloudmeta_message_text'))
    dp.register_message_handler(start.start_command, commands='start')
