from functools import wraps
import datetime
from bot.common import bot
from bot.db import db, DBTables
import asyncio
from aiogram import types


def not_allowed(message: types.Message, cd: int, by_id: bool):
    return asyncio.create_task(message.reply(
        text=
        f"❌ Wait for cooldown ({cd}s for this command)"
        f"{'. Please note that this cooldown is for all users' if not by_id else ''}"
    ))


def throttle(cooldown: int = 5, by_id: bool = True, admin_ids: list = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = int(args[0]["from"]["id"])
            if admin_ids and user_id in admin_ids:
                return asyncio.create_task(func(*args, **kwargs))
            user_id = str(user_id) if by_id else "0"
            now = datetime.datetime.now()
            delta = now - datetime.timedelta(seconds=cooldown)
            try:
                last_time = db[DBTables.cooldown].get(func.__name__).get(user_id)
            except AttributeError:
                last_time = None
            if not last_time:
                last_time = delta

            if last_time <= delta:
                try:
                    db[DBTables.cooldown][func.__name__][user_id] = now
                except KeyError:
                    db[DBTables.cooldown][func.__name__] = dict()
                    db[DBTables.cooldown][func.__name__][user_id] = now
                try:
                    return asyncio.create_task(func(*args, **kwargs))
                except Exception as e:
                    assert e
            else:
                return not_allowed(*args, cooldown, by_id)

        return wrapper

    return decorator
