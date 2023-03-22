from ... import utils
from .. import python
from ..mixins import IsConfigurableMixin


class TestFramework(IsConfigurableMixin, python.TestFramework):
    NEAREST_SEPARATOR = "."

    framework = "nose2"  # type: str
    pattern = r"(^|[\b_\.-])[Tt]est.*\.py$"  # type: str

    @classmethod
    def is_configurable_fallback(cls, _):
        return utils.is_executable("nose2")

    def build_file_position_args(self):
        return [self.get_module()]

    def build_line_position_args(self):
        args = self.build_file_position_args()
        nearest = self.find_nearest()

        return [self.NEAREST_SEPARATOR.join(args + nearest.namespaces + nearest.tests)]
