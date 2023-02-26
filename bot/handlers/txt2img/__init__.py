from bot.common import dp
from .txt2img import generate_command
from .set_settings import (
    set_height_command, set_negative_prompt_command, set_size_command, set_steps_command, set_width_command,
    set_prompt_command, set_sampler_command, set_cfg_scale_command, set_restore_faces_command
)


def register():
    dp.register_message_handler(txt2img.generate_command, commands='generate')
    dp.register_message_handler(set_settings.set_prompt_command, commands='setprompt')
    dp.register_message_handler(set_settings.set_height_command, commands='setheight')
    dp.register_message_handler(set_settings.set_width_command, commands='setwidth')
    dp.register_message_handler(set_settings.set_negative_prompt_command, commands='setnegative')
    dp.register_message_handler(set_settings.set_size_command, commands='setsize')
    dp.register_message_handler(set_settings.set_steps_command, commands='setsteps')
    dp.register_message_handler(set_settings.set_sampler_command, commands='setsampler')
    dp.register_message_handler(set_settings.set_cfg_scale_command, commands='setscale')
    dp.register_message_handler(set_settings.set_restore_faces_command, commands='setfaces')
