from ...cache import cache
from .. import java
from . import build_tool


class TestFramework(java.TestFramework):
    framework = "junit"  # type: str
    pattern = r"([Tt]est.*|.*[Tt]est(s|Case)?)\.java$"  # type: str

    @property
    @cache
    def build_tool(self):
        return build_tool.find(self.context.file)

    def build_executable(self):
        wrapper = self.file("{}w".format(self.build_tool.executable))
        command = (
            "./{}".format(wrapper.relpath)
            if wrapper.exists()
            else self.build_tool.executable
        )

        return [command, "test"]

    def build_suite_position_args(self):
        config_file = self.build_tool.config_file
        parent_config_file = self.build_tool.find_config_file(config_file.parent())

        if parent_config_file:
            return self.build_tool.build_module_args(
                parent_config_file.dir().relpath(config_file.dir().path),
            )

        return []

    def build_file_position_args(self):
        return (
            self.build_suite_position_args()
            + self.build_tool.build_file_position_args()
        )

    def build_line_position_args(self):
        args = self.build_tool.build_line_position_args(self.find_nearest())

        if args:
            return self.build_suite_position_args() + args
        else:
            return self.build_file_position_args()
