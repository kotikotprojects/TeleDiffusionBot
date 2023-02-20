from rich import print


def register_handlers():
    from bot.handlers import (
        initialize, admin, help_command, txt2img
    )

    initialize.register()
    admin.register()
    help_command.register()
    txt2img.register()

    print('[gray]All handlers registered[/]')
