from .. import TestFramework as BaseTestFramework


class TestFramework(BaseTestFramework):
    language = 'go'  # type: str
    pattern = r'[^_].*_test\.go$'  # type: str
