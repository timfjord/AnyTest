import os.path

from ... import utils
from .. import python
from ..mixins import IsConfigurableMixin


class TestFramework(IsConfigurableMixin, python.TestFramework):
    NEAREST_SEPARATOR = '.'

    framework = 'pyunit'
    pattern = r'test.*\.py$'

    @classmethod
    def is_configurable_fallback(cls, _):
        return utils.is_executable('python')

    def build_executable(self):
        return self.prefix_executable(['python', '-m', 'unittest'])

    def build_file_position_args(self):
        file_path = os.path.splitext(self.context.file.relpath)[0]

        return [file_path.replace(os.path.sep, self.NEAREST_SEPARATOR)]

    def build_line_position_args(self):
        file_args = self.build_file_position_args()
        nearest = self.find_nearest()

        return [
            self.NEAREST_SEPARATOR.join(file_args + nearest.namespaces + nearest.tests)
        ]
