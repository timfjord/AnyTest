from .. import errors
from ..outputs import Output as BaseOutput
from ..mixins import WindowMixin


class Output(BaseOutput, WindowMixin):
    name = 'panel'

    def panel_command(self):
        command = self.settings('command', type=str)

        if not command:
            raise errors.InvalidOutputCommand

        return command

    def options(self):
        options = {
            'shell_cmd': self.command.command,
            'working_dir': self.command.directory,
            'encoding': 'utf-8',
            'env': self.test_framework.settings(
                'env', default={}, fallback=False, type=dict, merge=True
            ),
        }

        if self.test_framework.output_file_regex is not None:
            options['file_regex'] = self.test_framework.output_file_regex

        return options

    def build(self):
        self.run_command(self.panel_command(), self.options())
