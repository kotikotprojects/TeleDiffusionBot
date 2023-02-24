from bot.db import db, DBTables, decrypt
import aiohttp
import asyncio
import time


async def job_exists(endpoint):
    async with aiohttp.ClientSession() as session:
        r = await session.get(
            endpoint + "/sdapi/v1/progress",
            json={
                "skip_current_image": True,
            }
        )
        if r.status != 200:
            return None
        return (await r.json()).get('state').get('job_count') > 0


async def wait_for_status(ignore_exceptions: bool = False):
    endpoint = decrypt(db[DBTables.config].get('endpoint'))
    try:
        while await job_exists(endpoint):
            while db[DBTables.cooldown].get('_last_time_status_checked', 0) + 5 > time.time():
                await asyncio.sleep(5)
            db[DBTables.cooldown]['_last_time_status_checked'] = time.time()
        return
    except Exception as e:
        if not ignore_exceptions:
            raise e
        return
