from aiogram import types
from bot.db import db, DBTables
from bot.utils.cooldown import throttle
from bot.modules.api.objects.prompt_request import Prompt
from bot.keyboards.exception import get_exception_keyboard
from bot.utils.trace_exception import PrettyException


@throttle(cooldown=5, admin_ids=db[DBTables.config].get('admins'))
async def set_prompt_command(message: types.Message):
    temp_message = await message.reply("⏳ Setting prompt...")
    if not message.get_args():
        await temp_message.edit_text("😶‍🌫️ Specify prompt for this command. Check /help setprompt")
        return

    try:
        prompt: Prompt = db[DBTables.prompts].get(message.from_id, Prompt(message.get_args()))
        prompt.prompt = message.get_args()
        prompt.creator = message.from_id
        db[DBTables.prompts][message.from_id] = prompt

        await db[DBTables.config].write()

        await message.reply('✅ Default prompt set')
        await temp_message.delete()

    except Exception as e:
        exception_id = f'{message.message_thread_id}-{message.message_id}'
        db[DBTables.exceptions][exception_id] = PrettyException(e)
        await message.reply('❌ Error happened while processing your request', parse_mode='html',
                            reply_markup=get_exception_keyboard(exception_id))
        await temp_message.delete()
        db[DBTables.queue]['n'] = db[DBTables.queue].get('n', 1) - 1
        return
