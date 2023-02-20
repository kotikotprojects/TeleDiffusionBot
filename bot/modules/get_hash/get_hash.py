import os
from bot.common import bot
import hashlib
import aiohttp


async def get_hash(file_id: str):
    url = bot.get_file_url(
        (await bot.get_file(file_id)).file_path
    )

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            assert resp.status == 200
            data = await resp.read()

    with open('file_to_get_hash', "wb") as f:
        f.write(data)

    file_hash = hashlib.md5(open('file_to_get_hash', 'rb').read()).hexdigest()

    os.remove('file_to_get_hash')
    return file_hash
