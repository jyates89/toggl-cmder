from togglcmder.toggl.caching import Caching
from togglcmder.toggl.downloader import Downloader
from togglcmder.toggl.commands import Commands


# Helpers that don't fit anywhere else!
def retrieve_downloader_from_context(context: dict) -> Downloader:
    downloader = context['downloader']
    assert(isinstance(downloader, Downloader))
    return downloader


def retrieve_cache_from_context(context: dict) -> Caching:
    caching = context['cache']
    assert(isinstance(caching, Caching))
    return caching


def retrieve_commands_from_context(context: dict) -> Commands:
    commands = context['commands']
    assert(isinstance(commands, Commands))
    return commands
