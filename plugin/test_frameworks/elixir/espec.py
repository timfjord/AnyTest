from .. import elixir


class TestFramework(elixir.TestFramework):
    framework = "espec"
    pattern = r"_spec\.exs$"

    def build_file_position_args(self):
        return [self.context.file.relpath]

    def build_line_position_args(self):
        return ["{}:{}".format(self.context.file.relpath, self.context.sel_line())]
