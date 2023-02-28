from ...utils import match_patterns
from .. import swift


class TestFramework(swift.TestFramework):
    NAMESPACE_SEPARATOR = '.'
    NEAREST_SEPARATOR = '/'

    framework = 'xctest'
    pattern = r'^Tests[/\\].*\.swift$'

    def build_file_position_args(self):
        filter, _ = match_patterns(self.context.file.relpath, self.module_patterns)

        if filter:
            namespace = self.context.find_nearest(self.namespace_patterns, from_line=1)
            return [
                '--filter',
                self.NAMESPACE_SEPARATOR.join([filter] + namespace.tests[0:1]),
            ]
        else:
            return []

    def build_line_position_args(self):
        args = self.build_file_position_args()

        if not bool(args):
            return []

        nearest = self.find_nearest()
        args[1] = self.NEAREST_SEPARATOR.join(args[1:2] + nearest.tests[0:1])

        return args
