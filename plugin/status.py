import sublime

from . import settings


def update(message):
    if not settings.get("show_status_messages", type=bool, default=True):
        return

    sublime.active_window().status_message(message)
