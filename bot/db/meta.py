import os.path
from bot.config import DBMETA, BARS_APP_ID, DB_CHAT
from bot.common import bot
from aiogram.utils.exceptions import MessageToForwardNotFound


class DBMeta:
    app_id = "app_id"
    message_id = "message_id"
    update_time = "update_time"

    def __init__(self):
        if not os.path.isfile(DBMETA):
            open(DBMETA, 'w').write(f'{BARS_APP_ID}|None|0')

    def __getitem__(self, item):
        try:
            return open(DBMETA).read().split('|')[{
                "app_id": 0,
                "message_id": 1,
                "update_time": 2
            }.get(item)]
        except TypeError:
            return None

    def __setitem__(self, key, value):
        meta = open(DBMETA).read().split('|')
        meta[{
            "app_id": 0,
            "message_id": 1,
            "update_time": 2
        }[key]] = value
        open(DBMETA, 'w').write('|'.join(str(x) for x in meta))

    def __str__(self):
        return open(DBMETA).read()


class CloudMeta:
    app_id = "app_id"
    message_id = "message_id"
    update_time = "update_time"

    @staticmethod
    async def get(item):
        try:
            try:
                if not DBMeta()[DBMeta.update_time] or not bot.cloudmeta_message_text:
                    raise AttributeError
            except AttributeError:
                try:
                    message = await bot.forward_message(DB_CHAT, DB_CHAT, DBMeta()[DBMeta.message_id])

                    bot.cloudmeta_message_text = message.caption

                    await message.delete()
                except MessageToForwardNotFound:
                    print('Cannot get CloudMeta - writing DBDict')
                    from .db_model import DBDict
                    await DBDict().write()
                    message = await bot.forward_message(DB_CHAT, DB_CHAT, DBMeta()[DBMeta.message_id])
                    bot.cloudmeta_message_text = message.caption
                    await message.delete()

            cloudmeta = bot.cloudmeta_message_text.split('|')
            return cloudmeta[{
                "app_id": 0,
                "message_id": 1,
                "update_time": 2
            }.get(item)]
        except TypeError:
            return None
