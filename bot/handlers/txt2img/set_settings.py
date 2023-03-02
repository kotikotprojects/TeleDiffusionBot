from aiogram import types
from bot.db import db, DBTables
from bot.utils.cooldown import throttle
from bot.modules.api.objects.prompt_request import Prompt
from bot.keyboards.exception import get_exception_keyboard
from bot.utils.trace_exception import PrettyException


async def _set_property(message: types.Message, prop: str, value=None):
    temp_message = await message.reply(f"⏳ Setting {prop}...")
    if not message.get_args():
        await temp_message.edit_text("😶‍🌫️ Specify arguments for this command. Check /help")
        return

    try:
        prompt: Prompt = db[DBTables.prompts].get(message.from_id)
        if prompt is None and prop != 'prompt':
            await temp_message.edit_text(f"You didn't created any prompt. Specify prompt text at least first time. "
                                         f"For example, it can be: <code>masterpiece, best quality, 1girl, white hair, "
                                         f"medium hair, cat ears, closed eyes, looking at viewer, :3, cute, scarf, "
                                         f"jacket, outdoors, streets</code>", parse_mode='HTML')
            return
        elif prompt is None:
            prompt = Prompt(message.get_args(), creator=message.from_id)

        prompt.__setattr__(prop, message.get_args() if value is None else value)
        prompt.creator = message.from_id
        db[DBTables.prompts][message.from_id] = prompt

        await db[DBTables.config].write()

        await message.reply(f'✅ {prop} set')
        await temp_message.delete()

    except Exception as e:
        exception_id = f'{message.message_thread_id}-{message.message_id}'
        db[DBTables.exceptions][exception_id] = PrettyException(e)
        await message.reply('❌ Error happened while processing your request', parse_mode='html',
                            reply_markup=get_exception_keyboard(exception_id))
        await temp_message.delete()
        db[DBTables.queue]['n'] = db[DBTables.queue].get('n', 1) - 1
        return


@throttle(cooldown=5, admin_ids=db[DBTables.config].get('admins'))
async def set_prompt_command(message: types.Message):
    await _set_property(message, 'prompt')


@throttle(cooldown=5, admin_ids=db[DBTables.config].get('admins'))
async def set_negative_prompt_command(message: types.Message):
    await _set_property(message, 'negative_prompt')


@throttle(cooldown=5, admin_ids=db[DBTables.config].get('admins'))
async def set_steps_command(message: types.Message):
    try:
        _ = int(message.get_args())
    except Exception as e:
        assert e
        await message.reply('❌ Specify number as argument')
        return

    if _ > 30:
        await message.reply('❌ Specify number <= 30')
        return

    await _set_property(message, 'steps')


@throttle(cooldown=5, admin_ids=db[DBTables.config].get('admins'))
async def set_cfg_scale_command(message: types.Message):
    try:
        _ = int(message.get_args())
    except Exception as e:
        assert e
        await message.reply('❌ Specify number as argument')
        return

    await _set_property(message, 'cfg_scale')


@throttle(cooldown=5, admin_ids=db[DBTables.config].get('admins'))
async def set_width_command(message: types.Message):
    try:
        _ = int(message.get_args())
    except Exception as e:
        assert e
        await message.reply('❌ Specify number as argument')
        return

    if _ > 768:
        await message.reply('❌ Specify number <= 768')
        return

    await _set_property(message, 'width')


@throttle(cooldown=5, admin_ids=db[DBTables.config].get('admins'))
async def set_height_command(message: types.Message):
    try:
        _ = int(message.get_args())
    except Exception as e:
        assert e
        await message.reply('❌ Specify number as argument')
        return

    if _ > 768:
        await message.reply('❌ Specify number <= 768')
        return

    await _set_property(message, 'height')


@throttle(cooldown=5, admin_ids=db[DBTables.config].get('admins'))
async def set_restore_faces_command(message: types.Message):
    try:
        _ = bool(message.get_args())
    except Exception as e:
        assert e
        await message.reply('❌ Specify boolean <code>True</code>/<code>False</code> as argument',
                            parse_mode='HTML')
        return

    await _set_property(message, 'restore_faces')


@throttle(cooldown=5, admin_ids=db[DBTables.config].get('admins'))
async def set_sampler_command(message: types.Message):
    temp_message = await message.reply('⏳ Getting samplers...')
    from bot.modules.api.samplers import get_samplers
    from aiohttp import ClientConnectorError
    try:
        if message.get_args() not in (samplers := await get_samplers()):
            await message.reply(
                f'❌ You can use only {", ".join(f"<code>{x}</code>" for x in samplers)}',
                parse_mode='HTML'
            )
            return
        await temp_message.delete()
    except ClientConnectorError:
        await message.reply('❌ Error! Maybe, StableDiffusion API endpoint is incorrect '
                            'or turned off')
        await temp_message.delete()
        return
    except Exception as e:
        exception_id = f'{message.message_thread_id}-{message.message_id}'
        db[DBTables.exceptions][exception_id] = PrettyException(e)
        await message.reply('❌ Error happened while processing your request', parse_mode='html',
                            reply_markup=get_exception_keyboard(exception_id))
        await temp_message.delete()
        return

    await _set_property(message, 'sampler')


@throttle(cooldown=5, admin_ids=db[DBTables.config].get('admins'))
async def set_size_command(message: types.Message):
    try:
        hxw = message.get_args().split('x')
        height = int(hxw[0])
        width = int(hxw[1])
    except Exception as e:
        assert e
        await message.reply('❌ Specify size in <code>hxw</code> format, for example <code>512x512</code>',
                            parse_mode='HTML')
        return

    if height > 768 or width > 768:
        await message.reply('❌ Specify numbers <= 768')
        return

    await _set_property(message, 'height', height)
    await _set_property(message, 'width', width)
