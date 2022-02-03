import sublime

from . import errors, runners

SETTINGS_KEY = 'AnyTest.history'


class History:
    """
    Window scoped history. The data is persisted in the window settings
    which makes it available even after package reload
    """

    def __init__(self):
        self._history = {}

    def settings(self):
        return sublime.active_window().settings()

    def add(self, runner):
        self.settings().set(
            SETTINGS_KEY, {'runner': runner.name, 'kwargs': runner.to_dict()}
        )

    def last(self):
        runnner_snapshot = self.settings().get(SETTINGS_KEY, None)

        if runnner_snapshot is None:
            raise errors.EmptyHistory

        runner = runners.load(runnner_snapshot['runner'])
        return runner(**runnner_snapshot['kwargs'])
