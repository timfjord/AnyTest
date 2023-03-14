from .. import TestFramework as BaseTestFramework


class TestFramework(BaseTestFramework):
    language = "python"
    test_patterns = (r"\s*(?:async )?def (test_\w+)",)
    namespace_patterns = (r"\s*class (\w+)",)

    def prefix_executable(self, executable):
        prefix = []

        if self.file("Pipfile").exists():
            prefix = ["pipenv", "run"]
        elif self.file("poetry.lock").exists():
            prefix = ["poetry", "run"]

        return prefix + executable
