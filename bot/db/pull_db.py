import os
from .meta import DBMeta, CloudMeta
from bot.common import bot
from bot.config import DB, DB_CHAT
from .db_model import DBTables
from sqlitedict import SqliteDict


async def pull():
    if DBMeta()[DBMeta.message_id] == 'None':
        from .db import db
        print('No dbmeta file')
        if msg_id := db[DBTables.config].get('db_message_id'):
            print('Found message id in in-db config')
            DBMeta()[DBMeta.message_id] = msg_id
        await db[DBTables.config].write()

    if not os.path.isfile('sync'):
        try:
            if not bot.cloudmeta_message_text:
                print('No cloudmeta initialized')
                raise AttributeError
            else:
                return
        except AttributeError:
            if int(DBMeta()[DBMeta.update_time]) >= int(await CloudMeta.get(CloudMeta.update_time)):
                print('First database pulling for this instance - DB is up-to-date')
                return
    else:
        print('Database file is new. Trying to download cloud data')
        os.remove('sync')

    print('DB is not up-to-date')

    message = await bot.forward_message(DB_CHAT, DB_CHAT, DBMeta()[DBMeta.message_id])

    await message.delete()

    await message.document.download(destination_file=DB + 'b')

    from .db import db
    for table in DBTables.tables:
        new_table = SqliteDict(DB + 'b', tablename=table)
        for key in new_table.keys():
            db[table][key] = new_table[key]
        new_table.close()

    print('Loaded database from cloud')
