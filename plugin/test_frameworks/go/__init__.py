from .. import TestFramework as BaseTestFramework


class TestFramework(BaseTestFramework):
    language = 'go'  # type: str
    test_patterns = (
        r'^\s*func ((Test|Example).*)\(',
        r'^\s*func \(.*\) ((Test).*)\(',
        r'^\s*t\.Run\("(.*)"',
    )
    namespace_patterns = (
        r'^\s*func ((Test).*)\(',
        r'^\s*t\.Run\("(.*)"',
    )
