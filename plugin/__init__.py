import logging
import operator

import sublime

from . import runners, settings, status, test_frameworks
from .context import Context
from .errors import Error, FrameworkNotFound, handle_errors
from .history import History
from .quick_panel_item import QuickPanelItem
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

    @handle_errors
    def select_test_framework(self, scope, edit=False):
        settings.reload_project_settings()

        items = sorted(
            test_frameworks.items(), key=operator.attrgetter('language', 'framework')
        )

        if len(items) == 1 and not settings.get('always_show_test_framework_selection'):
            self.run_test(scope, edit, items[0])
        else:
            self.view.window().show_quick_panel(
                [QuickPanelItem(item.framework, '', item.language) for item in items],
                lambda index: index != -1 and self.run_test(scope, edit, items[index]),
            )

    @handle_errors
    def run_test(self, scope, edit=False, test_framework=None):
        settings.reload_project_settings()

        try:
            runner = self.build_runner(scope, test_framework=test_framework)

            if edit and runner.editable:
                self.view.window().show_input_panel(
                    'Command',
                    runner.cmd,
                    lambda cmd: self.process_runner(runner, cmd),
                    lambda _: None,
                    lambda: None,
                )
            elif edit:
                raise Error("Runner '{}' is not editable".format(runner.name))
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

    def build_runner(self, scope, test_framework=None):
        if scope == SCOPE_LAST:
            return history.last()

        context = Context(self.view)
        if test_framework is None:
            test_framework = test_frameworks.find(context.file)

        runner = runners.find(test_framework)

        return runner.build(test_framework(context), scope)

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
