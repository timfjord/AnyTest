from .. import TestFramework as BaseTestFramework


class TestFramework(BaseTestFramework):
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
