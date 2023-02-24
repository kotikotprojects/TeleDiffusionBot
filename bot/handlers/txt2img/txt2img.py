from aiogram import types
from bot.db import db, DBTables
from bot.utils.cooldown import throttle
from bot.modules.api.txt2img import txt2img
from bot.modules.api.objects.prompt_request import Prompt
from bot.modules.api.status import wait_for_status
from bot.keyboards.exception import get_exception_keyboard
from bot.utils.trace_exception import PrettyException
from aiohttp import ClientConnectorError


@throttle(cooldown=30, admin_ids=db[DBTables.config].get('admins'))
async def txt2img_comand(message: types.Message):
    temp_message = await message.reply("⏳ Enqueued...")

    prompt: Prompt = db[DBTables.prompts].get(message.from_id)
    if not prompt:
        if message.get_args():
            db[DBTables.prompts][message.from_id] = Prompt(message.get_args(), creator=message.from_id)

    # TODO: Move it to other module

    try:
        db[DBTables.queue]['n'] = db[DBTables.queue].get('n', 0) + 1
        await temp_message.edit_text(f"⏳ Enqueued in position {db[DBTables.queue].get('n', 0)}...")

        await wait_for_status()

        await temp_message.edit_text(f"⌛ Generating...")
        prompt = Prompt(prompt=message.get_args(), creator=message.from_id)
        image = await txt2img(prompt)
        image_message = await message.reply_photo(photo=image[0])

        db[DBTables.queue]['n'] = db[DBTables.queue].get('n', 1) - 1
        db[DBTables.generated][image_message.photo[0].file_unique_id] = prompt

        await temp_message.delete()

        await db[DBTables.config].write()

    except ClientConnectorError:
        await message.reply('❌ Error! Maybe, StableDiffusion API endpoint is incorrect '
                            'or turned off')
        await temp_message.delete()
        db[DBTables.queue]['n'] = db[DBTables.queue].get('n', 1) - 1
        return

    except Exception as e:
        exception_id = f'{message.message_thread_id}-{message.message_id}'
        db[DBTables.exceptions][exception_id] = PrettyException(e)
        await message.reply('❌ Error happened while processing your request', parse_mode='html',
                            reply_markup=get_exception_keyboard(exception_id))
        await temp_message.delete()
        db[DBTables.queue]['n'] = db[DBTables.queue].get('n', 1) - 1
        return
