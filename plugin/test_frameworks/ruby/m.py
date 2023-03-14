from functools import lru_cache

from ... import settings
from .. import ruby


class TestFramework(ruby.TestFramework):
    framework = "m"
    pattern = r"_test\.rb$"

    @classmethod
    def is_suitable_for(cls, file):
        return super().is_suitable_for(file) and settings.get(
            ("ruby", "minitest", "use_m"), type=bool
        )

    @lru_cache(maxsize=None)
    def bin(self):
        return self.file("bin", "m")

    def build_executable(self):
        return self._build_executable("m", zeus=True, binstubs=True)

    def build_file_position_args(self):
        return [self.context.file.relpath]

    def build_line_position_args(self):
        return ["{}:{}".format(self.context.file.relpath, self.context.sel_line())]
