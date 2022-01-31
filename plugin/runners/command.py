from functools import lru_cache

from ..runners import Runner as BaseRunner
from ..mixins import WindowMixin


class Runner(BaseRunner, WindowMixin):
    name = 'command'

    @lru_cache(maxsize=None)
    def command_name(self):
        return self.settings('command', type=str, default='exec')

    @lru_cache(maxsize=None)
    def command_options(self):
        options = {
            'shell_cmd': self.command.cmd,
            'working_dir': self.command.dir,
            'encoding': 'utf-8',
            'env': self.test_framework.settings(
                'env', default={}, fallback=False, type=dict, merge=True
            ),
        }

        if self.test_framework.output_file_regex is not None:
            options['file_regex'] = self.test_framework.output_file_regex

        return options

    def run(self):
        self.run_command(self.command_name(), self.command_options())
