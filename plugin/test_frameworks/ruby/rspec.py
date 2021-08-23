from .. import ruby


class TestFramework(ruby.TestFramework):
    framework = 'rspec'
    pattern = r'(_spec\.rb|spec/.*\.feature)$'

    def build_executable(self):
        executable = './bin/rspec'

        return [executable]

    def build_nearest_position_args(self):
        return [
            '{}:{}'.format(self.context.file(), line) for line in self.context.lines()
        ]
