import os.path
from bot.config import DB
from .db_model import DBDict

if not os.path.isfile(DB):
    open('sync', 'w')


db = {
    'config': DBDict(DB, autocommit=True, tablename='config'),
    'cooldown': DBDict(DB, autocommit=True, tablename='cooldown'),
    'exceptions': DBDict(DB, autocommit=True, tablename='exceptions'),
    'queue': DBDict(DB, autocommit=True, tablename='queue'),
    'generated': DBDict(DB, autocommit=True, tablename='generated'),
    'actions': DBDict(DB, autocommit=True, tablename='actions'),
    'prompts': DBDict(DB, autocommit=True, tablename='prompts')
}
