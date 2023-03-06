from rich import print


def register_callbacks():
    from bot.callbacks import (
        exception,
        image_info,
        set_model
    )

    exception.register()
    image_info.register()
    set_model.register()

    print('[gray]All callbacks registered[/]')
