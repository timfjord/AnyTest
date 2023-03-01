import os.path
import re

from .. import go
from ..mixins import IsConfigurableMixin

REGEXP_ESCAPE_TRANSLATION_TABLE = str.maketrans(
    {
        '?': r'\\\?',
        '+': r'\\\+',
        '*': r'\\\*',
        '\\': r'\\\\',
        '^': r'\\\^',
        '$': r'\\\\\$',
        '.': r'\\\.',
        '|': r'\\\\\|',
        '{': r'\\\{',
        '}': r'\\\}',
        '[': r'\\\[',
        ']': r'\\\]',
        '(': r'\\\\\(',
        ')': r'\\\\\)',
    }
)


# TODO: This escape function doesn't work correctly with |()$^ symbols when the runner is `command`
def escape_regex(string):
    return string.translate(REGEXP_ESCAPE_TRANSLATION_TABLE)


class TestFramework(IsConfigurableMixin, go.TestFramework):
    NEAREST_SEPARATOR = '/'

    framework = 'gotest'  # type: str
    pattern = r'[^_].*_test\.go$'  # type: str

    def build_suite_position_args(self):
        return ['./...']

    def build_file_position_args(self):
        if self.context.file.dir().path == self.context.root.path:
            return []

        return ['./{}/...'.format(os.path.split(self.context.file.relpath)[0])]

    def build_line_position_args(self):
        args = self.build_file_position_args()
        name = re.sub(
            r'\s+',
            '_',
            self.find_nearest().join(
                self.NEAREST_SEPARATOR, end=r'\$', escape_regex=escape_regex
            ),
        )

        if bool(name):
            return ['-run', name] + (args if bool(args) else ['./.'])
        else:
            return args
