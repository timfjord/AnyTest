from .. import TestFramework as BaseTestFramework


class TestFramework(BaseTestFramework):
    language = "java"
    test_patterns = (r"^\s*(?:@Test\s+)?(?:public\s+)?void\s+(\w+)",)
    namespace_patterns = (r"^\s*(?:public\s+)?class\s+(\w+)",)
