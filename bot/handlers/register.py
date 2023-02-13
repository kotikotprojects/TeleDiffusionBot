from rich import print


def import_handlers():
    import bot.handlers.help.help
    assert bot.handlers.help.help

    import bot.handlers.initialize.pull_db
    assert bot.handlers.initialize.pull_db

    print('[gray]All handlers imported[/]')
