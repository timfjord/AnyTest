import sublime

from . import errors


class History:
    """
    Window scoped history
    """

    def __init__(self):
        self._history = {}

    @property
    def window_id(self):
        return sublime.active_window().id()

    def add(self, runner):
        self._history[self.window_id] = runner

    def last(self):
        try:
            return self._history[self.window_id]
        except KeyError:
            raise errors.EmptyHistory
