from bot.common import dp
from .txt2img import txt2img_comand


def register():
    dp.register_message_handler(txt2img.txt2img_comand, commands='txt2img')
