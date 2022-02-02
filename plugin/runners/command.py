from functools import lru_cache

from ..runners import Runner as BaseRunner


class Runner(BaseRunner):
    name = 'command'
    panel_name = 'output.exec'

    def __init__(self, test_framework, scope):
        super().__init__(test_framework, scope)

        panel_name = self.settings('panel_name', type=str)
        if panel_name:
            self.panel_name = panel_name

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
