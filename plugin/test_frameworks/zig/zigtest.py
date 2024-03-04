import shlex

from .. import zig


class TestFramework(zig.TestFramework):
    framework = "zigtest"  # type: str
    pattern = r".zig$"  # type: str

    test_patterns = (r'^\s*test\s+"(.+)"',)

    def build_suite_position_args(self):
        return ["build", "test"]

    def build_file_position_args(self):
        return ["test", self.context.file.relpath]

    def build_line_position_args(self):
        args = self.build_file_position_args()
        nearest = self.find_nearest()

        if not bool(nearest.tests):
            return args

        return args + [
            "--test-filter",
            shlex.quote(nearest.join("", escape_regex=True)),
        ]
