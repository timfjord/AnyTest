from . import outputs, settings, test_frameworks
from .command import Command
from .context import Context
from .errors import handle_errors
from .mixins import WindowMixin


SCOPE_LAST = 'last'


class Runner(WindowMixin):
    @classmethod
    def reload_project_settings(cls):
        settings.reload_project_settings()

    def __init__(self, view):
        self.view = view

    def window(self):
        return self.view.window()

    def save_file(self):
        if settings.get('save_all_files_on_run'):
            self.run_command('save_all')
        elif settings.get('save_current_file_on_run') and bool(self.view.file_name()):
            self.run_command('save')

    def build_command(self, scope):
        if scope == SCOPE_LAST:
            command = Command.last()
            test_framework = test_frameworks.load(command.language, command.framework)
        else:
            context = Context(self.view)
            test_framework = test_frameworks.find(context.file)
            command = Command.build(test_framework(context), scope)

        return command, test_framework

    @handle_errors
    def run_test(self, scope):
        command, test_framework = self.build_command(scope)
        output = outputs.find(test_framework)

        self.save_file()

        output(command, test_framework).build()
        command.save()
