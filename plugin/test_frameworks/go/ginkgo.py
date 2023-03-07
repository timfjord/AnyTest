import shlex

from ...cache import cache
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
    @cache
    def imports_ginkgo(cls, file):
        return file.contains_line('github.com/onsi/ginkgo')

    @classmethod
    def is_configurable_fallback(cls, file):
        return cls.imports_ginkgo(file)

    def build_suite_position_args(self):
        return ['./{}'.format(self.get_package())]

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
