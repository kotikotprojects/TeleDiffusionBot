import aiohttp
from bot.db import db, DBTables, decrypt


async def get_samplers():
    endpoint = decrypt(db[DBTables.config].get('endpoint'))
    async with aiohttp.ClientSession() as session:
        r = await session.get(endpoint + "/sdapi/v1/samplers")
        if r.status != 200:
            return None
    return [x["name"] for x in await r.json()]
