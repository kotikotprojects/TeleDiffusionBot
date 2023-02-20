from bot.common import dp
from .image_info import *


def register():
    dp.register_message_handler(imginfo, commands='imginfo')
