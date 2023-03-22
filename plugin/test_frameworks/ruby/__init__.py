import re
from functools import lru_cache

from .. import TestFramework as BaseTestFramework

_GEM_EMPTY_VERSION = (0, 0, 0)
_GEM_PATTERN = r"\s*{name}\s+\((\d+)\.(\d+)\.(\d+).*\)"


def get_gem_version(root, name):
    lockfile = root.file("Gemfile.lock")

    if not lockfile.exists():
        return _GEM_EMPTY_VERSION

    with open(lockfile.path) as file:
        for line in file:
            regex = _GEM_PATTERN.format(name=re.escape(name))
            match = re.findall(regex, line)
            if match:
                return tuple(map(int, match[0]))

    return _GEM_EMPTY_VERSION


def is_railties_5_or_greater(root):
    if not root.file("config", "application.rb").exists() and not any(
        root.glob("test", "*", "config", "application.rb")
    ):
        return False

    return get_gem_version(root, "railties")[0] >= 5


class TestFramework(BaseTestFramework):
    language = "ruby"  # type: str
    test_patterns = (
        (r"^\s*def\s+(test_\w+)", "test"),
        (r'^\s*test\s*[\( ]\s*(?:\"|\')(.*)(?:"|\')', "rails"),
        (r'^\s*it\s*[\( ]\s*(?:"|\')(.*)(?:"|\')', "spec"),
    )
    namespace_patterns = (
        r"^\s*(?:class|module)\s+(\S+)",
        r'^\s*describe\s*[\( ]\s*(?:"|\')(.*)(?:"|\')',
        r"^\s*describe\s*[\( ]\s*([^\s\)]+)",
    )

    def bin(self):
        raise NotImplementedError()

    @lru_cache(maxsize=None)
    def spring_bin(self):
        return self.file("bin", "spring")

    def _build_executable(self, command, zeus=False, spring=False, binstubs=False):
        executable = command if isinstance(command, list) else [command]

        if zeus and self.file(".zeus.sock").exists():
            executable = ["zeus"] + zeus if isinstance(zeus, list) else executable
        elif (
            spring
            and self.settings("use_spring_binstub")
            and self.spring_bin().exists()
        ):
            executable = [self.spring_bin().relpath] + executable
        elif binstubs and self.settings("use_binstubs") and self.bin().exists():
            executable = [self.bin().relpath] + (
                binstubs if isinstance(binstubs, list) else []
            )
        elif self.settings("use_bundle") and self.file("Gemfile").exists():
            executable = ["bundle", "exec"] + executable

        return executable
