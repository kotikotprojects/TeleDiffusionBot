import aiohttp
from bot.db import db, DBTables, decrypt
from .objects.prompt_request import Prompt
import json
import base64


async def txt2img(prompt: Prompt, ignore_exceptions: bool = False) -> list[bytes, dict] | None:
    endpoint = decrypt(db[DBTables.config].get('endpoint'))
    try:
        async with aiohttp.ClientSession() as session:
            r = await session.post(
                endpoint + "/sdapi/v1/txt2img",
                json={
                    "prompt": prompt.prompt,
                    "steps": prompt.steps,
                    "cfg_scale": prompt.cfg_scale,
                    "width": prompt.width,
                    "height": prompt.height,
                    "restore_faces": prompt.restore_faces,
                    "negative_prompt": prompt.negative_prompt,
                    "sampler_index": prompt.sampler
                }
            )
            if r.status != 200 and ignore_exceptions:
                return None
            elif r.status != 200:
                raise ValueError((await r.json())['detail'])
            return [base64.b64decode((await r.json())["images"][0]),
                    json.loads((await r.json())["info"])]
    except Exception as e:
        if not ignore_exceptions:
            raise e
        return
