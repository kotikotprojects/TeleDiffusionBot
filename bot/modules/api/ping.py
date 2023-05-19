import aiohttp
from bot.db import db, DBTables, decrypt


async def ping():
    endpoint = decrypt(db[DBTables.config].get('endpoint'))
    if endpoint is None:
        return False
    try:
        async with aiohttp.ClientSession() as session:
            r = await session.head(endpoint)
            if r.status != 200:
                return False
        return True
    except aiohttp.ClientConnectorError:
        return False
