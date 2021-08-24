from functools import lru_cache

import sublime

from .. import errors
from ..outputs import Output as BaseOutput


class Output(BaseOutput):
    name = 'panel'

    def window(self):
        return sublime.active_window()

    @lru_cache(maxsize=None)
    def sublime_command(self):
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
        self.window().run_command(self.sublime_command(), self.options())
