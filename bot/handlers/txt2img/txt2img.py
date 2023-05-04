import re
from bot.common import bot
from aiogram import types
from bot.db import db, DBTables
from bot.utils.cooldown import throttle
from bot.modules.api.txt2img import txt2img
from bot.modules.api.objects.get_prompt import get_prompt
from bot.modules.api.objects.prompt_request import Generated
from bot.modules.api.status import wait_for_status
from bot.keyboards.image_info import get_img_info_keyboard
from bot.utils.errorable_command import wrap_exception
from bot.callbacks.factories.image_info import (prompt_only, full_prompt, import_prompt, back)



@wrap_exception([ValueError], custom_loading=True)
@throttle(cooldown=30, admin_ids=db[DBTables.config].get('admins'))
async def generate_command(message: types.Message):
    temp_message = await message.reply("⏳ Enqueued...")
    if not db[DBTables.config]['enabled']:
        await message.reply('💔 Generation is disabled by admins now. Try again later')
        await temp_message.delete()
        return
    elif (message.chat.id not in db[DBTables.config]['whitelist'] and message.from_id not in db[DBTables.config]['whitelist']):
        await message.reply('❌You are not on the white list, access denied. Contact admin @kilisauros for details')
        await temp_message.delete()
        return

    try:
        prompt = get_prompt(user_id=message.from_id,
                            prompt_string=message.get_args())
    except AttributeError:
        await temp_message.edit_text(f"You didn't created any prompt. Specify prompt text at least first time. "
                                     f"For example, it can be: <code>masterpiece, best quality, 1girl, white hair, "
                                     f"medium hair, cat ears, closed eyes, looking at viewer, :3, cute, scarf, jacket, "
                                     f"outdoors, streets</code>", parse_mode='HTML')
        return

    try:
        db[DBTables.queue]['n'] = db[DBTables.queue].get('n', 0) + 1
        await temp_message.edit_text(f"⏳ Enqueued in position {db[DBTables.queue].get('n', 0)}...")

        await wait_for_status()

        await temp_message.edit_text(f"⌛ Generating...")
        db[DBTables.queue]['n'] = db[DBTables.queue].get('n', 1) - 1
        image = await txt2img(prompt)
        image_message = await message.reply_photo(photo=image[0])
        
        #Send photo to SD Image Archive
        # message_data = 

        archive_message = f'User ID:   {message.from_id} \n \
        User nickname:  {message.from_user.full_name} \n \
        User username:  @{message.from_user.username}'
        # archive_message = f'{callback_data=full_prompt.new(p_id=f"{image_message.photo[0].file_unique_id}")} + "User ID: " + message.from_id + " User nickname: " + message.from_user.full_name + " User username: " + message.from_user.username'
        await bot.send_photo(-929754401, photo=image[0], caption=archive_message, reply_markup=get_img_info_keyboard(image_message.photo[0].file_unique_id))


        db[DBTables.generated][image_message.photo[0].file_unique_id] = Generated(
            prompt=prompt,
            seed=image[1]['seed'],
            model=re.search(r", Model: ([^,]+),", image[1]['infotexts'][0]).groups()[0]
        )

        await message.reply('Here is your image',
                            reply_markup=get_img_info_keyboard(image_message.photo[0].file_unique_id))

        await temp_message.delete()

        await db[DBTables.config].write()

    except ValueError as e:
        await message.reply(f'❌ Error! {e.args[0]}')
        await temp_message.delete()
        db[DBTables.queue]['n'] = db[DBTables.queue].get('n', 1) - 1
        return
