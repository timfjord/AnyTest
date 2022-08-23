from AnyTest.tests import SublimeProjectTestCase


class VitestTestCase(SublimeProjectTestCase):
    folder = 'vitest'

    def test_line1(self):
        yield from self._testFile(('test', 'basic.test.ts'), 6)
        self.assertLastCommand(
            'vitest run -t \'Math\\.sqrt\\(\\)\' ', ('test', 'basic.test.ts')
        )

    def test_line2(self):
        yield from self._testFile(('test', 'suite.test.js'), 5)
        self.assertLastCommand(
            'vitest run -t \'suite name foo\' ', ('test', 'suite.test.js')
        )

    def test_line_no_nearest(self):
        yield from self._testFile(('test', 'basic.test.ts'), 1)
        self.assertLastCommand('vitest run ', ('test', 'basic.test.ts'))

    def test_file(self):
        yield from self._testFile(('test', 'basic.test.ts'))
        self.assertLastCommand('vitest run ', ('test', 'basic.test.ts'))

    def test_suite(self):
        yield from self._testSuite(('test', 'basic.test.ts'))
        self.assertLastCommand('vitest run')
