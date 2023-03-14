from functools import lru_cache

from .. import ruby


class TestFramework(ruby.TestFramework):
    framework = "rails"
    pattern = r"_test\.rb$"

    @classmethod
    def is_suitable_for(cls, file):
        return super().is_suitable_for(file) and ruby.is_railties_5_or_greater(
            file.root
        )

    @lru_cache(maxsize=None)
    def bin(self):
        return self.file("bin", "rails")

    def build_executable(self):
        return self._build_executable(
            ["rails", "test"], zeus=["test"], spring=True, binstubs=["test"]
        )

    def build_file_position_args(self):
        return [self.context.file.relpath]

    def build_line_position_args(self):
        return ["{}:{}".format(self.context.file.relpath, self.context.sel_line())]
