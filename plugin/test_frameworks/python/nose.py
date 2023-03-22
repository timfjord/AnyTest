from ... import utils
from .. import python
from ..mixins import IsConfigurableMixin


class TestFramework(IsConfigurableMixin, python.TestFramework):
    NEAREST_SEPARATOR = "."
    SEPARATOR = ":"

    framework = "nose"  # type: str
    pattern = r"(^|[\b_\.-])[Tt]est.*\.py$"  # type: str

    @classmethod
    def is_configurable_fallback(cls, _):
        return utils.is_executable("nosetests")

    def build_executable(self):
        return self._build_executable("nosetests")

    def build_file_position_args(self):
        return [self.context.file.relpath]

    def build_line_position_args(self):
        name = self.find_nearest().join(self.NEAREST_SEPARATOR)

        if bool(name):
            return [self.SEPARATOR.join([self.context.file.relpath, name])]
        else:
            return self.build_file_position_args()
