from bot.common import dp
from bot.db import db, DBTables
from aiogram import types
from .factories.image_info import full_prompt, prompt_only, import_prompt, back
from bot.keyboards.image_info import get_img_info_keyboard, get_img_back_keyboard
from bot.utils.cooldown import throttle
from bot.utils.private_keyboard import other_user
from bot.modules.api.objects.prompt_request import Prompt


async def on_back(call: types.CallbackQuery, callback_data: dict):
    p_id = callback_data['p_id']
    if await other_user(call):
        return

    await call.message.edit_text(
        "Image was generated using this bot",
        parse_mode='html',
        reply_markup=get_img_info_keyboard(p_id)
    )


@throttle(5)
async def on_prompt_only(call: types.CallbackQuery, callback_data: dict):
    p_id = callback_data['p_id']
    if await other_user(call):
        return

    prompt: Prompt = db[DBTables.generated].get(p_id)

    await call.message.edit_text(
        f"🖤 Prompt: {prompt.prompt} \n"
        f"{f'🐊 Negative: {prompt.negative_prompt}' if prompt.negative_prompt else ''}",
        parse_mode='html',
        reply_markup=get_img_back_keyboard(p_id)
    )


@throttle(5)
async def on_full_info(call: types.CallbackQuery, callback_data: dict):
    p_id = callback_data['p_id']
    if await other_user(call):
        return

    prompt: Prompt = db[DBTables.generated].get(p_id)

    await call.message.edit_text(
        f"🖤 Prompt: {prompt.prompt} \n"
        f"🐊 Negative: {prompt.negative_prompt} \n"
        f"🪜 Steps: {prompt.steps} \n"
        f"🧑‍🎨 CFG Scale: {prompt.cfg_scale} \n"
        f"🖥️ Size: {prompt.width}x{prompt.height} \n"
        f"😀 Restore faces: {'on' if prompt.restore_faces else 'off'} \n"
        f"⚒️ Sampler: {prompt.sampler}",
        parse_mode='html',
        reply_markup=get_img_back_keyboard(p_id)
    )


@throttle(5)
async def on_import(call: types.CallbackQuery, callback_data: dict):
    p_id = callback_data['p_id']
    if await other_user(call):
        return

    prompt: Prompt = db[DBTables.generated].get(p_id)

    await call.message.edit_text(
        f"😶‍🌫️ Not implemented yet",
        parse_mode='html',
        reply_markup=get_img_back_keyboard(p_id)
    )


def register():
    dp.register_callback_query_handler(on_prompt_only, prompt_only.filter())
    dp.register_callback_query_handler(on_back, back.filter())
    dp.register_callback_query_handler(on_full_info, full_prompt.filter())
    dp.register_callback_query_handler(on_import, import_prompt.filter())
