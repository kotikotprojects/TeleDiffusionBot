from bot.common import dp
from .aliases import *
from .reset import *
from .tools import *
from .on_off import *


def register():
    dp.register_message_handler(set_endpoint, commands='setendpoint')
    dp.register_message_handler(reset.resetqueue, commands='resetqueue')
    dp.register_message_handler(aliases.add_admin, commands='addadmin')
    dp.register_message_handler(aliases.remove_admin, commands='rmadmin')
    dp.register_message_handler(aliases.add_whitelist, commands='addwhitelist')
    dp.register_message_handler(aliases.remove_whitelist, commands='rmwhitelist')
    dp.register_message_handler(aliases.get_whitelist, commands='getwhitelist')
    dp.register_message_handler(tools.hash_command, commands='hash')
