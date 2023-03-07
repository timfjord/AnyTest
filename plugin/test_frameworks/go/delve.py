import shlex

from .. import go
from ..mixins import IsConfigurableMixin
from .ginkgo import TestFramework as Ginkgo
from .gotest import TestFramework as Gotest


class TestFramework(IsConfigurableMixin, go.TestFramework):
    framework = 'delve'  # type: str

    def build_suite_position_args(self):
        return ['./...']

    def build_file_position_args(self):
        if self.context.file.is_in_root():
            return []

        return ['./{}/...'.format(self.context.file.dir_relpath())]

    def build_line_position_args(self):
        is_ginkgo = Ginkgo.imports_ginkgo(self.context.file)
        test_framework = Ginkgo(self.context) if is_ginkgo else Gotest(self.context)
        nearest = test_framework.find_nearest()
        name = ' '.join(nearest.tests)

        if bool(name):
            args = ['./{}'.format(self.get_package())]

            if is_ginkgo:
                return args + ['--', '-ginkgo.focus={}'.format(shlex.quote(name))]
            else:
                return args + ['--', '-test.run', shlex.quote('{}$'.format(name))]
        else:
            return self.build_file_position_args()
