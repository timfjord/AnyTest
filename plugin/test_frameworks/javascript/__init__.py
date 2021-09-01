from .. import TestFramework as BaseTestFramework


class TestFramework(BaseTestFramework):
    language = 'javascript'
    test_patterns = (r'^\s*(?:it|test)\s*[\( ]\s*(?:"|\'|`)(.*)(?:"|\'|`)',)
    namespace_patterns = (
        r'^\s*(?:describe|suite|context)\s*[( ]\s*(?:"|\'|`)(.*)(?:"|\'|`)',
    )
