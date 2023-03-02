import os.path
import re

from ...utils import escape_regex
from .. import go
from ..mixins import IsConfigurableMixin


class TestFramework(IsConfigurableMixin, go.TestFramework):
    NEAREST_SEPARATOR = '/'

    framework = 'gotest'  # type: str
    pattern = r'[^_].*_test\.go$'  # type: str

    def build_suite_position_args(self):
        return ['./...']

    def build_file_position_args(self):
        tags = []
        for line in self.context.file.lines():
            if re.match(r'\s*package\s', line):
                break

            match = re.match(r'\s*//\s*\+build\s+(.+)', line)
            if match:
                tags.append(re.sub(r'\s+', ',', match.group(1)))

        if tags:
            tags = ['-tags={}'.format(','.join(tags))]

        if self.context.file.is_in_root():
            return tags

        return tags + ['./{}/...'.format(self.context.file.dir_relpath())]

    def build_line_position_args(self):
        args = self.build_file_position_args()
        name = re.sub(
            r'\s',
            '_',
            self.find_nearest().join(
                self.NEAREST_SEPARATOR,
                end='$',
                escape_regex=lambda x: escape_regex(escape_regex(x)),
            ),
        )

        if bool(name):
            args = ['-run', name] + args

            if not args[-1].startswith('./'):
                args = args + ['./.']

            return args
        else:
            return args
