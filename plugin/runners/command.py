from ..runners import Runner as BaseRunner


class Runner(BaseRunner):
    DEFAULT_COMMAND_NAME = 'exec'

    name = 'command'
    panel_name = 'output.exec'

    def get_panel_name(self):
        return self.options.pop('panel_name', self.__class__.panel_name)

    def get_command_name(self):
        return self.options.pop('command_name', self.DEFAULT_COMMAND_NAME)

    def get_command_options(self):
        return dict(
            self.options,
            **{
                'shell_cmd': self.cmd,
                'working_dir': self.dir,
            }
        )

    def run(self):
        self.run_command(self.get_command_name(), self.get_command_options())

    class Builder(BaseRunner.Builder):
        def build_options(self):
            options = {
                'command_name': Runner.settings('name', type=str),
                'encoding': 'utf-8',
                'env': self.test_framework.settings(
                    'env', default={}, fallback=False, type=dict, merge=True
                ),
            }

            if self.test_framework.output_file_regex is not None:
                options['file_regex'] = self.test_framework.output_file_regex

            return options
