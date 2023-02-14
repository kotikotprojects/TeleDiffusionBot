import aiohttp
from bot.db import db, DBTables
import json
import base64


async def txt2img(prompt: str, negative_prompt: str = None, steps: int = 20,
                  cfg_scale: int = 7, width: int = 768, height: int = 768,
                  restore_faces: bool = True, sampler: str = "Euler a") -> list[bytes, dict] | None:
    endpoint = db[DBTables.config].get('endpoint')
    try:
        async with aiohttp.ClientSession() as session:
            r = await session.post(
                endpoint + "/sdapi/v1/txt2img",
                json={
                    "prompt": prompt,
                    "steps": steps,
                    "cfg_scale": cfg_scale,
                    "width": width,
                    "height": height,
                    "restore_faces": restore_faces,
                    "negative_prompt": negative_prompt,
                    "sampler_index": sampler
                }
            )
            if r.status != 200:
                return None
            return [base64.b64decode((await r.json())["images"][0]),
                    json.loads((await r.json())["info"])]
    except Exception as e:
        assert e
        return None
