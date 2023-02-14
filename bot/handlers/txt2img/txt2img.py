from aiogram import types
from bot.db import db, DBTables
from bot.utils.cooldown import throttle
import os.path
from bot.modules.api.txt2img import txt2img


@throttle(cooldown=30, admin_ids=db[DBTables.config].get('admins'))
async def txt2img_comand(message: types.Message):
    temp_message = await message.reply("⏳ Generating image...")
    if not message.get_args():
        await temp_message.edit_text("Specify prompt for this command. Check /help txt2img")
        return

    if not os.path.isfile('adstring'):
        with open('adstring', 'w') as f:
            f.write('@aiistop_bot')

    try:
        image = await txt2img(message.get_args())
        await message.reply_photo(photo=image[0], caption=str(
            image[1]["infotexts"][0]) + "\n\n" + open('adstring').read())
    except Exception as e:
        assert e
        await message.reply("We ran into error while processing your request. StableDiffusion models may not be "
                            "configured on specified endpoint or server with StableDiffusion may be turned "
                            "off. Ask admins of this bot instance if you have contacts for further info")
        await temp_message.delete()
        return

    await temp_message.delete()
