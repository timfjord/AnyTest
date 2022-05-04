import logging

import sublime

from . import runners, settings, test_frameworks
from .context import Context
from .errors import Error, handle_errors
from .history import History
from .view_callbacks import ViewCallbacks

SCOPE_LAST = 'last'

history = History()

logger = logging.getLogger(__name__)


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
        self.runner = None

    def build_runner(self, scope):
        if scope == SCOPE_LAST:
            return history.last()

        context = Context(self.view)
        test_framework = test_frameworks.find(context.file)
        runner = runners.find(test_framework)

        return runner.build(test_framework(context), scope)

    @handle_errors
    def run_test(self, scope, edit=False):
        settings.reload_project_settings()

        self.runner = self.build_runner(scope)

        if edit:
            self.view.window().show_input_panel(
                'Command',
                self.runner.cmd,
                self.process_runner,
                lambda _: None,
                lambda: None,
            )
        else:
            self.process_runner()

    @handle_errors
    def process_runner(self, command=''):
        if self.runner is None:
            raise Error('Runner is not set')

        if bool(command):
            self.runner = self.runner._replace(cmd=command)

        ViewCallbacks(self.view).run()

        logger.debug("Running '%s' from '%s'", self.runner.cmd, self.runner.dir)
        self.runner.run()
        history.add(self.runner)
