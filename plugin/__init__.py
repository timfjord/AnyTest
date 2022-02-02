from . import runners, settings, test_frameworks
from .context import Context
from .errors import handle_errors
from .history import History
from .mixins import WindowMixin

SCOPE_LAST = 'last'

history = History()


class Plugin(WindowMixin):
    @classmethod
    @handle_errors
    def show_last_output(cls, focus=True):
        history.last().show_output(focus=focus)

    def __init__(self, view):
        self.view = view

    @property
    def window(self):
        return self.view.window()

    def save_file(self):
        if settings.get('save_all_files_on_run'):
            self.run_command('save_all')
        elif settings.get('save_current_file_on_run') and bool(self.view.file_name()):
            self.run_command('save')

    def build_runner(self, scope):
        if scope == SCOPE_LAST:
            return history.last()

        context = Context(self.view)
        test_framework = test_frameworks.find(context.file)
        runner = runners.find(test_framework)

        return runner(test_framework(context), scope)

    @handle_errors
    def run_test(self, scope):
        settings.reload_project_settings()

        runner = self.build_runner(scope)

        self.save_file()

        runner.run()
        history.add(runner)
