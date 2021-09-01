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
