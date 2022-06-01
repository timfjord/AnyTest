from functools import lru_cache

from .. import TestFramework as BaseTestFramework


class TestFramework(BaseTestFramework):
    BINSTUBS_WITH_PREFIX = 'prefix'

    language = 'ruby'
    test_patterns = (
        (r'^\s*def\s+(test_\w+)', 'test'),
        (r'^\s*test\s*[\( ]\s*(?:\"|\')(.*)(?:"|\')', 'rails'),
        (r'^\s*it\s*[\( ]\s*(?:"|\')(.*)(?:"|\')', 'spec'),
    )
    namespace_patterns = (
        r'^\s*(?:class|module)\s+(\S+)',
        r'^\s*describe\s*[\( ]\s*(?:"|\')(.*)(?:"|\')',
        r'^\s*describe\s*[\( ]\s*([^\s\)]+)',
    )

    def bin(self):
        raise NotImplementedError()

    def _build_executable(self, command, zeus=False, spring=False, binstubs=False):
        executable = command if isinstance(command, list) else [command]

        if zeus and self.file('.zeus.sock').exists():
            executable = ['zeus'] + executable
        elif (
            spring
            and self.settings('use_spring_binstub')
            and self.spring_bin().exists()
        ):
            executable = [self.spring_bin().relpath] + executable
        elif binstubs and self.settings('use_binstubs') and self.bin().exists():
            executable = [self.bin().relpath] + (
                executable if binstubs == self.BINSTUBS_WITH_PREFIX else []
            )
        elif self.settings('use_bundle') and self.file('Gemfile').exists():
            executable = ['bundle', 'exec'] + executable

        return executable
