import os.path
from bot.config import DB
from .db_model import DBDict

if not os.path.isfile(DB):
    open('sync', 'w')


db = {
    'config': DBDict(DB, autocommit=True, tablename='config'),
    'cooldown': DBDict(DB, autocommit=True, tablename='cooldown')
}
