import logging

import sublime

from . import runners, settings, status, test_frameworks
from .context import Context
from .errors import Error, FrameworkNotFound, handle_errors
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

    def build_runner(self, scope, quite_panel_item=None):
        if scope == SCOPE_LAST:
            return history.last()

        context = Context(self.view)
        test_framework = (
            test_frameworks.find(context.file)
            if quite_panel_item is None
            else test_frameworks.load(*quite_panel_item.signature())
        )

        runner = runners.find(test_framework)

        return runner.build(test_framework(context), scope)

    @handle_errors
    def select_test_framework(self, scope, edit=False):
        items = test_frameworks.quick_panel_items()

        self.view.window().show_quick_panel(
            items,
            lambda index: index != -1 and self.run_test(scope, edit, items[index]),
        )

    @handle_errors
    def run_test(self, scope, edit=False, quite_panel_item=None):
        settings.reload_project_settings()

        try:
            runner = self.build_runner(scope, quite_panel_item=quite_panel_item)

            if edit:
                self.view.window().show_input_panel(
                    'Command',
                    runner.cmd,
                    lambda cmd: self.process_runner(runner, cmd),
                    lambda _: None,
                    lambda: None,
                )
            else:
                self.process_runner(runner)
        except FrameworkNotFound as exc:
            if (
                settings.get('select_test_framework_when_not_found')
                and scope != SCOPE_LAST
            ):
                status.update("Couldn't find a test framework, please select one")
                self.view.run_command(
                    'any_test_run', {'scope': scope, 'edit': edit, 'select': True}
                )
            else:
                raise exc

    @handle_errors
    def process_runner(self, runner, cmd=''):
        if runner is None:
            raise Error('Runner is not set')

        if bool(cmd):
            runner = runner._replace(cmd=cmd)

        ViewCallbacks(self.view).run()

        logger.debug("Running '%s' from '%s'", runner.cmd, runner.dir)
        runner.run()
        history.add(runner)
