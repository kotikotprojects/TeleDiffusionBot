import aiohttp
import json
from bot.db import db, DBTables, decrypt


async def get_models() -> list | None:
    endpoint = decrypt(db[DBTables.config].get('endpoint'))
    async with aiohttp.ClientSession() as session:
        r = await session.get(endpoint + '/sdapi/v1/sd-models')
        if r.status != 200:
            return None
        json_data = await r.json()
    return [x["title"] for x in json_data]


async def set_model(model_name: str):
    endpoint = decrypt(db[DBTables.config].get('endpoint'))
    async with aiohttp.ClientSession() as session:
        r = await session.post(endpoint + "/sdapi/v1/options", json={
            "sd_model_checkpoint": model_name
        })
        if r.status != 200:
            return False
    return True
