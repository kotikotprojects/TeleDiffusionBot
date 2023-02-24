from rich import print


def register_callbacks():
    from bot.callbacks import (
        exception,
        image_info
    )

    exception.register()
    image_info.register()

    print('[gray]All callbacks registered[/]')
