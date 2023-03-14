import sublime

from . import errors, runners


class History:
    """
    Window scoped history. The data is persisted in the window settings
    which makes it available even after package reload
    """

    SETTINGS_KEY = "AnyTest.history.items"
    MAX_ITEMS = 10

    @classmethod
    def current(cls):
        return cls(sublime.active_window())

    def __init__(self, window):
        self._window = window

    @property
    def _settings(self):
        return self._window.settings()

    @property
    def items(self):
        return self._settings.get(self.SETTINGS_KEY, [])

    @items.setter
    def items(self, value):
        self._settings.set(self.SETTINGS_KEY, value)

    def add(self, runner):
        data = {"runner": runner.name, "kwargs": runner.to_dict()}
        items = [
            item
            for item in self.items
            if item["kwargs"]["cmd"] != runner.cmd
            or item["kwargs"]["dir"] != runner.dir
        ]

        new_items = [data] + items[: (self.MAX_ITEMS - 1)]
        self.items = new_items

    def clear(self):
        self.items = []

    @property
    def runners(self):
        return (runners.load(item["runner"])(**item["kwargs"]) for item in self.items)

    def last(self):
        try:
            return next(self.runners)
        except StopIteration:
            raise errors.EmptyHistory
