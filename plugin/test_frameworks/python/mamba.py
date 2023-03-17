from ... import utils
from .. import python
from ..mixins import IsConfigurableMixin


class TestFramework(IsConfigurableMixin, python.TestFramework):
    framework = "mamba"
    pattern = r"_spec\.py$"

    @classmethod
    def is_configurable_fallback(cls, _):
        return utils.is_executable("mamba")

    def build_executable(self):
        return self._build_executable("mamba")

    def build_file_position_args(self):
        return [self.context.file.relpath]

    def build_line_position_args(self):
        return self.build_file_position_args()
