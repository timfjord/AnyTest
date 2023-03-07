import os
import re
import shlex

from .. import javascript
from ..mixins import IsConfigurableMixin


class TestFramework(IsConfigurableMixin, javascript.TestFramework):
    framework = 'mocha'
    pattern = r'(tests?[/\\].*|(test))\.(js|jsx|coffee|ts|tsx)$'

    @classmethod
    def is_configurable_fallback(cls, file):
        return javascript.has_package('mocha', file.root)

    def build_executable(self):
        executable = 'mocha-webpack' if self.has_package('mocha-webpack') else 'mocha'

        return self._build_executable(executable)

    def args(self):
        args = super().args()

        if self.has_package('ts-node'):
            args = ['-r', os.path.join('ts-node', 'register')] + args

        return args

    def build_suite_position_args(self):
        test_dir = self.context.file.relpath.split(os.sep)[0]

        if re.match(r'tests?$', test_dir):
            return ['--recursive', test_dir + '/'] + (
                ['--extension', 'ts'] if self.has_package('ts-node') else []
            )

        parts = self.context.file.relpath.split('.')
        return [
            os.path.join(
                '"{}'.format(test_dir),
                '**',
                '*.{}.{}"'.format(parts[-2], parts[-1]),
            )
        ]

    def build_file_position_args(self):
        return [self.context.file.relpath]

    def build_line_position_args(self):
        args = self.build_file_position_args()
        name = self.find_nearest().join(' ', namespace_start='^', test_end='$')

        if bool(name):
            args += ['--grep', shlex.quote(name)]

        return args
