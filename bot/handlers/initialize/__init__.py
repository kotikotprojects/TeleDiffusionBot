from bot.common import dp, bot
from .start import *
from .all_messages import *
from bot.db import db, DBTables


def register():
    dp.register_message_handler(all_messages.sync_db_filter, lambda *_: not hasattr(bot, 'cloudmeta_message_text'))
    dp.register_message_handler(all_messages.on_action_message,
                                lambda message: str(message.from_id) in list(db[DBTables.actions].keys()))
    dp.register_message_handler(start.start_command, commands='start')
