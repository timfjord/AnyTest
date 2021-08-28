from functools import lru_cache

from .. import ruby


class TestFramework(ruby.TestFramework):
    framework = 'rspec'
    pattern = r'(_spec\.rb|spec/.*\.feature)$'

    @lru_cache(maxsize=None)
    def spring_bin(self):
        return self.file('bin', 'spring')

    @lru_cache(maxsize=None)
    def bin(self):
        return self.file('bin', 'rspec')

    def build_executable(self):
        executable = ['rspec']

        if self.file('.zeus.sock').exists():
            executable = ['zeus', 'rspec']
        elif self.spring_bin().exists() and self.settings('use_spring_binstub'):
            executable = [self.spring_bin().relpath, 'rspec']
        elif self.bin().exists() and self.settings('use_binstubs'):
            executable = [self.bin().relpath]
        elif self.file('Gemfile').exists() and self.settings('bundle_exec'):
            executable = ['bundle', 'exec', 'rspec']

        return executable

    def build_nearest_position_args(self):
        return [
            '{}:{}'.format(self.context.file.relpath, line)
            for line in self.context.lines()
        ]

    def build_file_position_args(self):
        return [self.context.file.relpath]
