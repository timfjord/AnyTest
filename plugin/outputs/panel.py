import sublime

from .. import errors
from ..outputs import Output as BaseOutput


class Output(BaseOutput):
    settings_key = 'panel'

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
        sublime_command = self.settings('command', type=str)

        if sublime_command:
            sublime.active_window().run_command(sublime_command, self.options())

            if self.settings('focus_on_run'):
                pass  # TODO: Implement me
        else:
            raise errors.InvalidOutputCommand
