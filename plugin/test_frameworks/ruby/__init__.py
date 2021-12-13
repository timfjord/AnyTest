from functools import lru_cache

from .. import TestFramework as BaseTestFramework


class TestFramework(BaseTestFramework):
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

    @lru_cache(maxsize=None)
    def use_zeus(self):
        return self.file('.zeus.sock').exists()

    def zeus(self, executable):
        return ['zeus'] + executable

    def bin(self):
        raise NotImplementedError()

    @lru_cache(maxsize=None)
    def use_binstubs(self):
        return self.bin().exists() and self.settings('use_binstubs')

    @lru_cache(maxsize=None)
    def use_bundler(self):
        return self.file('Gemfile').exists() and self.settings('bundle_exec')

    def bundle(self, executable):
        return ['bundle', 'exec'] + executable
