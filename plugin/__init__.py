import sublime

from . import runners, settings, test_frameworks
from .context import Context
from .errors import handle_errors
from .history import History
from .view_callbacks import ViewCallbacks

SCOPE_LAST = 'last'

history = History()


class Plugin:
    @classmethod
    @handle_errors
    def show_last_output(cls, focus=True):
        history.last().show_output(focus=focus)

    @classmethod
    @handle_errors
    def edit_last(cls):
        runner = history.last()
        sublime.active_window().open_file(
            '{}:{}'.format(runner.file, runner.line), sublime.ENCODED_POSITION
        )

    def __init__(self, view):
        self.view = view

    def build_runner(self, scope):
        if scope == SCOPE_LAST:
            return history.last()

        context = Context(self.view)
        test_framework = test_frameworks.find(context.file)
        runner = runners.find(test_framework)

        return runner.build(test_framework(context), scope)

    @handle_errors
    def run_test(self, scope):
        settings.reload_project_settings()

        runner = self.build_runner(scope)

        ViewCallbacks(self.view).run()

        runner.run()
        history.add(runner)
