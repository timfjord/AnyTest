from .. import ruby


class TestFramework(ruby.TestFramework):
    framework = 'rspec'
    pattern = r'(_spec\.rb|spec/.*\.feature)$'

    def build_executable(self):
        executable = ['rspec']

        if self.context.file_exist('.zeus.sock'):
            executable = ['zeus', 'rspec']
        elif self.context.file_exist('bin', 'spring') and self.settings(
            'use_spring_binstub'
        ):
            executable = ['./bin/spring', 'rspec']
        elif self.context.file_exist('bin', 'rspec') and self.settings('use_binstubs'):
            executable = ['./bin/rspec']
        elif self.context.file_exist('Gemfile') and self.settings('bundle_exec'):
            executable = ['bundle', 'exec', 'rspec']

        return executable

    def build_nearest_position_args(self):
        return [
            '{}:{}'.format(self.context.file(), line) for line in self.context.lines()
        ]

    def build_file_position_args(self):
        return [self.context.file()]
