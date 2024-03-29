from ... import utils
from .. import python
from ..mixins import IsConfigurableMixin


class TestFramework(IsConfigurableMixin, python.TestFramework):
    NEAREST_SEPARATOR = "."

    framework = "pyunit"  # type: str
    pattern = r"test.*\.py$"  # type: str

    @classmethod
    def is_configurable_fallback(cls, _):
        return utils.is_executable("python")

    def build_executable(self):
        return self._build_executable(["python", "-m", "unittest"])

    def build_file_position_args(self):
        return [self.get_module()]

    def build_line_position_args(self):
        args = self.build_file_position_args()
        nearest = self.find_nearest()

        return [self.NEAREST_SEPARATOR.join(args + nearest.namespaces + nearest.tests)]
