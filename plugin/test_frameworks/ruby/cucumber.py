from functools import lru_cache

from .. import ruby


class TestFramework(ruby.TestFramework):
    framework = "cucumber"
    pattern = r"features[/\\].*\.feature"

    @classmethod
    def is_suitable_for(cls, file):
        return super().is_suitable_for(file) and any(
            file.root.glob("features", "**", "*.rb")
        )

    @lru_cache(maxsize=None)
    def bin(self):
        return self.file("bin", "cucumber")

    def build_executable(self):
        return self._build_executable("cucumber", zeus=True, binstubs=True)

    def build_file_position_args(self):
        return [self.context.file.relpath]

    def build_line_position_args(self):
        return ["{}:{}".format(self.context.file.relpath, self.context.sel_line())]
