from AnyTest.tests import SublimeProjectTestCase


class SwiftPMTestCase(SublimeProjectTestCase):
    folder = 'swiftpm'

    def test_line(self):
        yield from self._testFile(('Tests', 'VimTestTests', 'VimTestTests.swift'), 6)
        self.assertLastCommand(
            'swift test --filter VimTestTests.VimTestTests/testExample'
        )

        self._testLine(10)
        self.assertLastCommand(
            'swift test --filter VimTestTests.VimTestTests/testOther'
        )

    def test_file(self):
        yield from self._testFile(('Tests', 'VimTestTests', 'VimTestTests.swift'))
        self.assertLastCommand('swift test --filter VimTestTests.VimTestTests')

    def test_file_final_test_cases(self):
        yield from self._testFile(('Tests', 'VimTestTests', 'VimTestFinalTests.swift'))
        self.assertLastCommand('swift test --filter VimTestTests.VimTestFinalTests')

    def test_file_public_test_cases(self):
        yield from self._testFile(('Tests', 'VimTestTests', 'VimTestPublicTests.swift'))
        self.assertLastCommand('swift test --filter VimTestTests.VimTestPublicTests')

    def test_file_public_final_test_cases(self):
        yield from self._testFile(
            ('Tests', 'VimTestTests', 'VimTestPublicFinalTests.swift')
        )
        self.assertLastCommand(
            'swift test --filter VimTestTests.VimTestPublicFinalTests'
        )

    def test_file_final_public_test_cases(self):
        yield from self._testFile(
            ('Tests', 'VimTestTests', 'VimTestFinalPublicTests.swift')
        )
        self.assertLastCommand(
            'swift test --filter VimTestTests.VimTestFinalPublicTests'
        )

    def test_file_test_cases_in_the_root_of_the_test_directory(self):
        yield from self._testFile(('Tests', 'VimTestRootTests.swift'))
        self.assertLastCommand('swift test --filter VimTestRootTests.VimTestRootTests')

    def test_suite(self):
        yield from self._testSuite(('Tests', 'VimTestTests', 'VimTestTests.swift'))
        self.assertLastCommand('swift test')
