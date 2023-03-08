from rich import print


def register_callbacks():
    from bot.callbacks import (
        exception,
        image_info,
        set_model,
        common
    )

    exception.register()
    image_info.register()
    set_model.register()
    common.register()

    print('[gray]All callbacks registered[/]')
