from .. import javascript, escape
from ..mixins import SuitableMixin


class TestFramework(SuitableMixin, javascript.TestFramework):
    framework = 'jest'
    pattern = r'(__tests__/.*|(spec|test))\.(js|jsx|coffee|ts|tsx)$'

    @classmethod
    def is_suitable(cls, file):
        return javascript.has_package('jest', file.root)

    def bin(self):
        return self.file('node_modules', '.bin', 'jest')

    def build_executable(self):
        if self.bin().exists():
            return [self.bin().relpath]
        else:
            return ['jest']

    def build_nearest_position_args(self):
        args = self.build_file_position_args()
        nearest = self.find_nearest()

        name = ''.join(
            (
                '^' if bool(nearest.namespaces) else '',
                escape.regex(' '.join(nearest.namespaces + nearest.tests)),
                '$' if bool(nearest.tests) else '',
            )
        )

        if bool(name):
            args = ['-t', escape.shell(name)] + args

        return args

    def build_file_position_args(self):
        return ['--', self.context.file.relpath]
