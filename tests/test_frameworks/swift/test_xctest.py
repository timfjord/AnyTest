from AnyTest.tests import SublimeProjectTestCase


class XCTestTestCase(SublimeProjectTestCase):
    folder = "xctest"

    def test_line(self):
        yield from self._testFile(("Tests", "AnyTestTests", "AnyTestTests.swift"), 6)
        self.assertLastCommand(
            "swift test --filter AnyTestTests.AnyTestTests/testExample"
        )

        self._testLine(10)
        self.assertLastCommand(
            "swift test --filter AnyTestTests.AnyTestTests/testOther"
        )

    def test_file(self):
        yield from self._testFile(("Tests", "AnyTestTests", "AnyTestTests.swift"))
        self.assertLastCommand("swift test --filter AnyTestTests.AnyTestTests")

    def test_file_final_test_cases(self):
        yield from self._testFile(("Tests", "AnyTestTests", "AnyTestFinalTests.swift"))
        self.assertLastCommand("swift test --filter AnyTestTests.AnyTestFinalTests")

    def test_file_public_test_cases(self):
        yield from self._testFile(("Tests", "AnyTestTests", "AnyTestPublicTests.swift"))
        self.assertLastCommand("swift test --filter AnyTestTests.AnyTestPublicTests")

    def test_file_public_final_test_cases(self):
        yield from self._testFile(
            ("Tests", "AnyTestTests", "AnyTestPublicFinalTests.swift")
        )
        self.assertLastCommand(
            "swift test --filter AnyTestTests.AnyTestPublicFinalTests"
        )

    def test_file_final_public_test_cases(self):
        yield from self._testFile(
            ("Tests", "AnyTestTests", "AnyTestFinalPublicTests.swift")
        )
        self.assertLastCommand(
            "swift test --filter AnyTestTests.AnyTestFinalPublicTests"
        )

    def test_file_test_cases_in_the_root_of_the_test_directory(self):
        yield from self._testFile(("Tests", "AnyTestRootTests.swift"))
        self.assertLastCommand("swift test --filter AnyTestRootTests.AnyTestRootTests")

    def test_suite(self):
        yield from self._testSuite(("Tests", "AnyTestTests", "AnyTestTests.swift"))
        self.assertLastCommand("swift test")
