from bot.common import dp
from .txt2img import *


def register():
    dp.register_message_handler(txt2img, commands='txt2img')
