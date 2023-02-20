from rich import print


def register_callbacks():
    from bot.callbacks import (
        exception
    )

    exception.register()

    print('[gray]All callbacks registered[/]')
