import os

from .. import ruby


class TestFramework(ruby.TestFramework):
    framework = "test_bench"  # type: str
    pattern = r"(^|/|\\)test[/\\]automated[/\\].+\.rb$"  # type: str

    def build_executable(self):
        return self._build_executable("bench")

    def build_suite_position_args(self):
        return [os.path.join("test", "automated", "")]

    def build_file_position_args(self):
        return [self.context.file.relpath]

    def build_line_position_args(self):
        return self.build_file_position_args()
