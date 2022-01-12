from functools import lru_cache

from .. import ruby


class TestFramework(ruby.TestFramework):
    framework = 'rspec'
    pattern = r'(_spec\.rb|spec[/\\].*\.feature)$'

    @lru_cache(maxsize=None)
    def spring_bin(self):
        return self.file('bin', 'spring')

    @lru_cache(maxsize=None)
    def bin(self):
        return self.file('bin', 'rspec')

    def build_executable(self):
        executable = ['rspec']

        if self.use_zeus():
            executable = self.zeus(executable)
        elif self.spring_bin().exists() and self.settings('use_spring_binstub'):
            executable = [self.spring_bin().relpath] + executable
        elif self.use_binstubs():
            executable = [self.bin().relpath]
        elif self.use_bundler():
            executable = self.bundle(executable)

        return executable

    def build_file_position_args(self):
        return [self.context.file.relpath]

    def build_line_position_args(self):
        return [
            '{}:{}'.format(self.context.file.relpath, line)
            for line in self.context.sel_lines()
        ]
