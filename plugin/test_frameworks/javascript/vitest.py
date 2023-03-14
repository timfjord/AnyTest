import shlex

from .. import javascript
from ..mixins import IsConfigurableMixin


class TestFramework(IsConfigurableMixin, javascript.TestFramework):
    framework = "vitest"
    pattern = r"(test[/\\].*|(spec|test))\.(js|jsx|coffee|ts|tsx)$"

    @classmethod
    def is_configurable_fallback(cls, file):
        return javascript.has_package("vitest", file.root)

    def build_executable(self):
        return self._build_executable("vitest") + ["run"]

    def build_file_position_args(self):
        return [self.context.file.relpath]

    def build_line_position_args(self):
        args = self.build_file_position_args()
        name = self.find_nearest().join(" ", escape_regex=True)

        if bool(name):
            args = ["-t", shlex.quote(name)] + args

        return args
