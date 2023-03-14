from .. import TestFramework as BaseTestFramework


class TestFramework(BaseTestFramework):
    language = "swift"
    test_patterns = (r"^\s*func (test.*)\(\)",)
    namespace_patterns = (
        r"^(?:(?:public )?(?:final )?|(?:final )?(?:public )?)class ([-_a-zA-Z0-9]+): XCTestCase",
    )
    module_patterns = (r"^Tests[/\\]([-_ a-zA-Z0-9]+)(?:[/\\]|\.swift)",)
