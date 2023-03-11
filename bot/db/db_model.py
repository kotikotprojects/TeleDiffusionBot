from sqlitedict import SqliteDict
from bot.common import bot
from bot.config import DB_CHAT, DB
from aiogram.types import InputFile, InputMediaDocument
from aiogram.utils.exceptions import MessageToEditNotFound
import time
from .meta import DBMeta


class DBTables:
    tables = ['config', 'cooldown', 'exceptions', 'queue', 'generated', 'actions', 'prompts']
    config = "config"
    cooldown = "cooldown"
    exceptions = "exceptions"
    queue = "queue"
    generated = "generated"
    actions = "actions"
    prompts = "prompts"


class DBDict(SqliteDict):
    async def write(self):
        try:
            DBMeta()[DBMeta.update_time] = time.time_ns()
            await bot.edit_message_media(media=InputMediaDocument(InputFile(DB)),
                                         chat_id=DB_CHAT, message_id=DBMeta()[DBMeta.message_id])
            await bot.edit_message_caption(
                caption=DBMeta(), chat_id=DB_CHAT, message_id=DBMeta()[DBMeta.message_id]
            )
        except MessageToEditNotFound:
            DBMeta()[DBMeta.update_time] = time.time_ns()
            self['db_message_id'] = (await bot.send_document(chat_id=DB_CHAT, document=InputFile(DB),
                                                             disable_notification=True)).message_id
            DBMeta()[DBMeta.message_id] = self['db_message_id']
            await bot.edit_message_caption(
                caption=DBMeta(), chat_id=DB_CHAT, message_id=self.get('db_message_id')
            )
