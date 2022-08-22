from .. import javascript, utils
from ..mixins import IsConfigurableMixin


class TestFramework(IsConfigurableMixin, javascript.TestFramework):
    EOO = '--'  # end of the options

    framework = 'jest'
    pattern = r'(__tests__[/\\].*|(spec|test))\.(js|jsx|coffee|ts|tsx)$'

    @classmethod
    def is_configurable_fallback(cls, file):
        return javascript.has_package('jest', file.root)

    def build_executable(self):
        return self._build_executable('jest')

    def build_file_position_args(self):
        return [self.EOO, self.context.file.relpath]

    def build_line_position_args(self):
        args = self.build_file_position_args()
        nearest = self.find_nearest()

        name = ''.join(
            (
                '^' if bool(nearest.namespaces) else '',
                utils.escape_regex(' '.join(nearest.namespaces + nearest.tests)),
                '$' if bool(nearest.tests) else '',
            )
        )

        if bool(name):
            args = ['-t', utils.escape_shell(name)] + args

        return args

    def build_command(self, scope):
        command = super().build_command(scope)

        if any(part and part.endswith('yarn') for part in command):
            command.remove(self.EOO)

        return command
