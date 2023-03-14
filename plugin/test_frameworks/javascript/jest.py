import shlex

from .. import javascript
from ..mixins import IsConfigurableMixin


class TestFramework(IsConfigurableMixin, javascript.TestFramework):
    EOO = "--"  # end of the options

    framework = "jest"
    pattern = r"(__tests__[/\\].*|(spec|test))\.(js|jsx|coffee|ts|tsx)$"

    @classmethod
    def is_configurable_fallback(cls, file):
        return javascript.has_package("jest", file.root)

    def build_executable(self):
        return self._build_executable("jest")

    def build_file_position_args(self):
        return [self.EOO, self.context.file.relpath]

    def build_line_position_args(self):
        args = self.build_file_position_args()
        name = self.find_nearest().join(
            " ", namespace_start="^", test_end="$", escape_regex=True
        )

        if bool(name):
            args = ["-t", shlex.quote(name)] + args

        return args

    def build_command(self, scope):
        command = super().build_command(scope)

        if any(part and part.endswith("yarn") for part in command):
            command.remove(self.EOO)

        return command
