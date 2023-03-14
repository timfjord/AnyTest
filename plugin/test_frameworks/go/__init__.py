from .. import TestFramework as BaseTestFramework


class TestFramework(BaseTestFramework):
    language = "go"  # type: str
    pattern = r"[^_].*_test\.go$"  # type: str

    def get_package(self):
        return (
            "." if self.context.file.is_in_root() else self.context.file.dir_relpath()
        )
