from bot.modules.api.objects.prompt_request import Prompt
from bot.db import db, DBTables


def get_prompt(user_id: int, prompt_string: str = None, negative_prompt: str = None, steps: int = None,
               cfg_scale: int = None, width: int = None, height: int = None, restore_faces: bool = None,
               sampler: str = None) -> Prompt:
    new_prompt: Prompt = db[DBTables.prompts].get(user_id)
    creator = user_id
    if not new_prompt:
        if user_id and prompt_string:
            db[DBTables.prompts][user_id] = Prompt(
                prompt=prompt_string,
                creator=user_id,
                negative_prompt=negative_prompt,
                steps=steps,
                cfg_scale=cfg_scale,
                width=width,
                height=height,
                restore_faces=restore_faces,
                sampler=sampler,
            )
            new_prompt: Prompt = db[DBTables.prompts].get(user_id)
        else:
            raise AttributeError('No prompt string specified and prompt doesn\'t exist for this user')

    if prompt_string:
        new_prompt.prompt = prompt_string

    for key in new_prompt.__dict__.keys():
        if key in locals().keys() and locals()[key]:
            new_prompt.__setattr__(key, locals()[key])
        elif not new_prompt.__getattribute__(key):
            new_prompt.__setattr__(key, Prompt('').__getattribute__(key))

    db[DBTables.prompts][user_id] = new_prompt

    return new_prompt
