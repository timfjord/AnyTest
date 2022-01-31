from functools import lru_cache

import sublime

from . import errors


class History:
    """
    Window scoped history
    """

    def __init__(self):
        self._history = {}

    @lru_cache(maxsize=None)
    def window_id(self):
        return sublime.active_window().id()

    def add(self, runner):
        self._history[self.window_id()] = runner

    def last(self):
        last = self._history.get(self.window_id(), None)

        if last is None:
            raise errors.EmptyHistory

        return last
