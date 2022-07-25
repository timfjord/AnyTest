import re
from functools import lru_cache

from .. import ruby

_GEM_EMPTY_VERSION = (0, 0, 0)
_GEM_PATTERN = r'\s*{name}\s+\((\d+)\.(\d+)\.(\d+).*\)'


def get_gem_version(root, name):
    lockfile = root.file('Gemfile.lock')

    if not lockfile.exists():
        return _GEM_EMPTY_VERSION

    with open(lockfile.path) as file:
        for line in file:
            regex = _GEM_PATTERN.format(name=re.escape(name))
            match = re.findall(regex, line)
            if match:
                return tuple(map(int, match[0]))

    return _GEM_EMPTY_VERSION


class TestFramework(ruby.TestFramework):
    framework = 'rails'
    pattern = r'_test\.rb$'

    @classmethod
    def is_suitable_for(cls, file):
        if not super().is_suitable_for(file):
            return False

        if not file.root.file('config', 'application.rb').exists() and not any(
            file.root.glob('test', '*', 'config', 'application.rb')
        ):
            return False

        return get_gem_version(file.root, 'railties')[0] >= 5

    @lru_cache(maxsize=None)
    def bin(self):
        return self.file('bin', 'rails')

    def build_executable(self):
        return self._build_executable(
            ['rails', 'test'], zeus=['test'], spring=True, binstubs=['test']
        )

    def build_file_position_args(self):
        return [self.context.file.relpath]

    def build_line_position_args(self):
        return ['{}:{}'.format(self.context.file.relpath, self.context.sel_line())]
