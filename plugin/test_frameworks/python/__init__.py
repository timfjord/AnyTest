import os.path

from .. import TestFramework as BaseTestFramework


class TestFramework(BaseTestFramework):
    MODULE_SEPARATOR = "."

    language = "python"  # type: str
    test_patterns = (r"\s*(?:async )?def (test_\w+)",)
    namespace_patterns = (r"\s*class (\w+)",)

    def _build_executable(self, command):
        executable = command if isinstance(command, list) else [command]
        prefix = []

        if self.file("Pipfile").exists():
            prefix = ["pipenv", "run"]
        elif self.file("poetry.lock").exists():
            prefix = ["poetry", "run"]
        elif self.file("pdm.lock").exists():
            prefix = ["pdm", "run"]

        return prefix + executable

    def get_module(self):
        path, _ = os.path.splitext(self.context.file.relpath)

        return path.replace(os.sep, self.MODULE_SEPARATOR)
