import shlex

from .. import go
from ..mixins import IsConfigurableMixin


class TestFramework(IsConfigurableMixin, go.TestFramework):
    NEAREST_SEPARATOR = '/'

    framework = 'ginkgo'  # type: str
    test_patterns = (
        r'^\s*It\("(.*)",',
        r'^\s*When\("(.*)",',
        r'^\s*Context\("(.*)",',
        r'.*Describe\("(.*)",',
    )
    namespace_patterns = ()

    @classmethod
    def is_configurable_fallback(cls, file):
        return file.contains_line('github.com/onsi/ginkgo')

    def build_suite_position_args(self):
        if self.context.file.is_in_root():
            return ['./.']

        return ['./{}'.format(self.context.file.dir_relpath())]

    def build_file_position_args(self):
        return [
            '--focus-file={}'.format(self.context.file.relpath)
        ] + self.build_suite_position_args()

    def build_line_position_args(self):
        nearest = self.find_nearest()

        if bool(nearest.tests):
            return [
                '--focus={}'.format(shlex.quote(nearest.tests[0]))
            ] + self.build_suite_position_args()
        else:
            return self.build_file_position_args()
