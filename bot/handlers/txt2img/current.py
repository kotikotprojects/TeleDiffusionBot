from aiogram import types
from bot.db import db, DBTables
from bot.utils.cooldown import throttle
from bot.modules.api.objects.prompt_request import Prompt
from bot.utils.errorable_command import wrap_exception


@wrap_exception()
@throttle(cooldown=5, admin_ids=db[DBTables.config].get('admins', []))
async def get_current(message: types.Message):
    prompt: Prompt = db[DBTables.prompts].get(message.from_id)
    if prompt is None:
        await message.reply('❌ No prompts found for you')

    await message.reply(
        f"🖤 Prompt: {prompt.prompt} \n"
        f"🐊 Negative: {prompt.negative_prompt} \n"
        f"🪜 Steps: {prompt.steps} \n"
        f"🧑‍🎨 CFG Scale: {prompt.cfg_scale} \n"
        f"🖥️ Size: {prompt.width}x{prompt.height} \n"
        f"😀 Restore faces: {'on' if prompt.restore_faces else 'off'} \n"
        f"⚒️ Sampler: {prompt.sampler} \n",
        parse_mode='html'
    )
