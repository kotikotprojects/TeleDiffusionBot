from functools import wraps
import datetime
from bot.db import db, DBTables
import asyncio
from aiogram import types


def not_allowed(message: types.Message, cd: int, by_id: bool):
    text = f"❌ Wait for cooldown ({cd}s for this command) " \
           f"{'. Please note that this cooldown is for all users' if not by_id else ''}"
    return asyncio.create_task(message.reply(
        text=text
    ) if hasattr(message, 'reply') else message.answer(text=text, show_alert=True))


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
                    f_name_dict = db[DBTables.cooldown][func.__name__]
                    f_name_dict[user_id] = now
                    db[DBTables.cooldown][func.__name__] = f_name_dict
                except KeyError:
                    f_name_dict = dict()
                    f_name_dict[user_id] = now
                    db[DBTables.cooldown][func.__name__] = f_name_dict
                try:
                    return asyncio.create_task(func(*args, **kwargs))
                except Exception as e:
                    assert e 
            else:
                return not_allowed(*args, cooldown, by_id)

        return wrapper

    return decorator
