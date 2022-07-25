from functools import lru_cache

from .. import ruby


class TestFramework(ruby.TestFramework):
    framework = 'rspec'
    pattern = r'(_spec\.rb|spec[/\\].*\.feature)$'

    @lru_cache(maxsize=None)
    def bin(self):
        return self.file('bin', 'rspec')

    def build_executable(self):
        return self._build_executable('rspec', zeus=True, spring=True, binstubs=True)

    def build_file_position_args(self):
        return [self.context.file.relpath]

    def build_line_position_args(self):
        return [
            '{}:{}'.format(self.context.file.relpath, line)
            for line in self.context.sel_lines()
        ]
