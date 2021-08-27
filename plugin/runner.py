from . import errors, settings, test_frameworks
from .command import Command


SCOPE_LAST = 'last'


class Runner:
    def __init__(self, context):
        self.context = context

    def run(self, scope):
        command, test_framework = (
            Command.last()
            if scope == SCOPE_LAST
            else Command.from_framework(self.framework(), scope)
        )

        if settings.get('save_all_files_on_run'):
            self.context.run_command('save_all')
        elif settings.get('save_current_file_on_run'):
            self.context.run_command('save')

        command.run(test_framework)

    def framework(self):
        for framework in test_frameworks.items():
            if framework.is_suitable_for(self.context.file()):
                return framework(self.context)
        else:
            raise errors.FrameworkNotFound
