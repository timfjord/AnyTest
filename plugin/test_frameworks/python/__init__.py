from .. import TestFramework as BaseTestFramework


class TestFramework(BaseTestFramework):
    language = 'python'
    test_patterns = (r'\s*(?:async )?def (test_\w+)',)
    namespace_patterns = (r'\s*class (\w+)',)
