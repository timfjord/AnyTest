from .. import python, utils
from ..mixins import IsConfigurableMixin


class TestFramework(IsConfigurableMixin, python.TestFramework):
    NEAREST_SEPARATOR = '::'

    framework = 'pytest'
    pattern = r'(test_[^/\\]+|[^/\\]+_test)\.py$'

    @classmethod
    def is_configurable_fallback(cls, _):
        return utils.is_executable('pytest') or utils.is_executable('py.test')

    def build_executable(self):
        executable = ['python', '-m', 'pytest']

        if utils.is_executable('pytest'):
            executable = ['pytest']
        elif utils.is_executable('py.test'):
            executable = ['py.test']

        return self.prefix_executable(executable)

    def build_file_position_args(self):
        return [self.context.file.relpath]

    def build_line_position_args(self):
        file_args = self.build_file_position_args()
        nearest = self.find_nearest()

        return [
            self.NEAREST_SEPARATOR.join(file_args + nearest.namespaces + nearest.tests)
        ]
