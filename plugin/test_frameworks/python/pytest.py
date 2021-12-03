from .. import python, utils
from ..mixins import IsConfigurableMixin


class TestFramework(IsConfigurableMixin, python.TestFramework):
    NEAREST_SEPARATOR = '::'

    framework = 'pytest'
    pattern = r'(test_[^/]+|[^/]+_test)\.py$'

    @classmethod
    def is_configurable_fallback(cls, _):
        return utils.is_executable('pytest') or utils.is_executable('py.test')

    def build_executable(self):
        if utils.is_executable('py.test') and not utils.is_executable('pytest'):
            executable = ['py.test']
        else:
            executable = ['pytest']

        if self.file('Pipfile').exists():
            executable = ['pipenv', 'run'] + executable
        elif self.file('poetry.lock').exists():
            executable = ['poetry', 'run'] + executable

        return executable

    def build_nearest_position_args(self):
        file_args = self.build_file_position_args()
        nearest = self.find_nearest()

        return [
            self.NEAREST_SEPARATOR.join(file_args + nearest.namespaces + nearest.tests)
        ]

    def build_file_position_args(self):
        return [self.context.file.relpath]
