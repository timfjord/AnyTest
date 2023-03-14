import re

from ...utils import escape_regex
from .. import go
from ..mixins import IsConfigurableMixin


class TestFramework(IsConfigurableMixin, go.TestFramework):
    NEAREST_SEPARATOR = "/"

    framework = "gotest"  # type: str
    test_patterns = (
        r"^\s*func ((Test|Example).*)\(",
        r"^\s*func \(.*\) ((Test).*)\(",
        r'^\s*t\.Run\("(.*)"',
    )
    namespace_patterns = (
        r"^\s*func ((Test).*)\(",
        r'^\s*t\.Run\("(.*)"',
    )

    def build_suite_position_args(self):
        return ["./..."]

    def build_tags_args(self):
        tags = []
        for line in self.context.file.lines():
            if re.match(r"\s*package\s", line):
                break

            match = re.match(r"\s*//\s*\+build\s+(.+)", line)
            if match:
                tags.append(re.sub(r"\s+", ",", match.group(1)))

        if tags:
            tags = ["-tags={}".format(",".join(tags))]

        return tags

    def build_file_position_args(self):
        args = self.build_tags_args()

        if self.context.file.is_in_root():
            return args

        return args + ["./{}/...".format(self.context.file.dir_relpath())]

    def build_line_position_args(self):
        args = self.build_file_position_args()
        name = re.sub(
            r"\s",
            "_",
            self.find_nearest().join(
                self.NEAREST_SEPARATOR,
                end="$",
                escape_regex=lambda x: escape_regex(escape_regex(x)),
            ),
        )

        if bool(name):
            return (
                ["-run", name]
                + self.build_tags_args()
                + ["./{}".format(self.get_package())]
            )
        else:
            return args
