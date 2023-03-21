from .. import python


class TestFramework(python.TestFramework):
    framework = "behave"  # type: str
    pattern = r"\.feature$"  # type: str

    @classmethod
    def is_suitable_for(cls, file):
        return super().is_suitable_for(file) and any(
            file.root.glob("features", "**", "*.py")
        )

    def build_file_position_args(self):
        return [self.context.file.relpath]

    def build_line_position_args(self):
        return ["{}:{}".format(self.context.file.relpath, self.context.sel_line())]
