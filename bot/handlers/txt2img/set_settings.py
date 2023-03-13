from aiogram import types
from bot.db import db, DBTables
from bot.utils.cooldown import throttle
from bot.modules.api.objects.prompt_request import Prompt
from bot.utils.errorable_command import wrap_exception


@wrap_exception(custom_loading=True)
async def _set_property(message: types.Message, prop: str, value=None, is_command: bool = True):
    temp_message = await message.reply(f"⏳ Setting {prop}...")
    if not message.get_args() and is_command:
        await temp_message.edit_text("😶‍🌫️ Specify arguments for this command. Check /help")
        return

    prompt: Prompt = db[DBTables.prompts].get(message.from_id)
    if prompt is None and prop != 'prompt':
        await temp_message.edit_text(f"You didn't created any prompt. Specify prompt text at least first time. "
                                     f"For example, it can be: <code>masterpiece, best quality, 1girl, white hair, "
                                     f"medium hair, cat ears, closed eyes, looking at viewer, :3, cute, scarf, "
                                     f"jacket, outdoors, streets</code>", parse_mode='HTML')
        return
    elif prompt is None:
        prompt = Prompt((message.get_args() if is_command else message.text), creator=message.from_id)

    prompt.__setattr__(prop, (message.get_args() if is_command else message.text) if value is None else value)
    prompt.creator = message.from_id
    db[DBTables.prompts][message.from_id] = prompt

    await db[DBTables.config].write()

    await message.reply(f'✅ {prop} set')
    await temp_message.delete()


@throttle(cooldown=5, admin_ids=db[DBTables.config].get('admins'))
async def set_prompt_command(message: types.Message, is_command: bool = True):
    await _set_property(message, 'prompt', is_command=is_command)


@throttle(cooldown=5, admin_ids=db[DBTables.config].get('admins'))
async def set_negative_prompt_command(message: types.Message, is_command: bool = True):
    await _set_property(message, 'negative_prompt', is_command=is_command)


@throttle(cooldown=5, admin_ids=db[DBTables.config].get('admins'))
async def set_steps_command(message: types.Message, is_command: bool = True):
    try:
        _ = int((message.get_args() if is_command else message.text))
    except Exception as e:
        assert e
        await message.reply('❌ Specify number as argument')
        return

    if _ > 30:
        await message.reply('❌ Specify number <= 30')
        return

    await _set_property(message, 'steps', is_command=is_command)


@throttle(cooldown=5, admin_ids=db[DBTables.config].get('admins'))
async def set_cfg_scale_command(message: types.Message, is_command: bool = True):
    try:
        _ = int((message.get_args() if is_command else message.text))
    except Exception as e:
        assert e
        await message.reply('❌ Specify number as argument')
        return

    await _set_property(message, 'cfg_scale', is_command=is_command)


@throttle(cooldown=5, admin_ids=db[DBTables.config].get('admins'))
async def set_width_command(message: types.Message, is_command: bool = True):
    try:
        _ = int((message.get_args() if is_command else message.text))
    except Exception as e:
        assert e
        await message.reply('❌ Specify number as argument')
        return

    if _ > 768 or _ < 256:
        await message.reply('❌ Specify number <= 768 and >= 256')
        return

    await _set_property(message, 'width', is_command=is_command)


@throttle(cooldown=5, admin_ids=db[DBTables.config].get('admins'))
async def set_height_command(message: types.Message, is_command: bool = True):
    try:
        _ = int((message.get_args() if is_command else message.text))
    except Exception as e:
        assert e
        await message.reply('❌ Specify number as argument')
        return

    if _ > 768 or _ < 256:
        await message.reply('❌ Specify number <= 768 and >= 256')
        return

    await _set_property(message, 'height', is_command=is_command)


@throttle(cooldown=5, admin_ids=db[DBTables.config].get('admins'))
async def set_restore_faces_command(message: types.Message, is_command: bool = True):
    try:
        _ = bool((message.get_args() if is_command else message.text))
    except Exception as e:
        assert e
        await message.reply('❌ Specify boolean <code>True</code>/<code>False</code> as argument',
                            parse_mode='HTML')
        return

    await _set_property(message, 'restore_faces', is_command=is_command)


@wrap_exception()
@throttle(cooldown=5, admin_ids=db[DBTables.config].get('admins'))
async def set_sampler_command(message: types.Message, is_command: bool = True):
    from bot.modules.api.samplers import get_samplers
    if (message.get_args() if is_command else message.text) not in (samplers := await get_samplers()):
        await message.reply(
            f'❌ You can use only {", ".join(f"<code>{x}</code>" for x in samplers)}',
            parse_mode='HTML'
        )
        return

    await _set_property(message, 'sampler', is_command=is_command)


@throttle(cooldown=5, admin_ids=db[DBTables.config].get('admins'))
async def set_size_command(message: types.Message, is_command: bool = True):
    try:
        hxw = (message.get_args() if is_command else message.text).split('x')
        height = int(hxw[0])
        width = int(hxw[1])
    except Exception as e:
        assert e
        await message.reply('❌ Specify size in <code>hxw</code> format, for example <code>512x512</code>',
                            parse_mode='HTML')
        return

    if height > 768 or width > 768 or height < 256 or width < 256:
        await message.reply('❌ Specify numbers <= 768 and >= 256')
        return

    await _set_property(message, 'height', height, is_command=is_command)
    await _set_property(message, 'width', width, is_command=is_command)
