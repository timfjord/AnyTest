from AnyTest.tests import SublimeProjectTestCase


class CucumberTestCase(SublimeProjectTestCase):
    folder = 'cucumber'

    def test_line(self):
        yield from self._testFile(('features', 'normal.feature'), 1)
        self.assertLastCommand('cucumber features/normal.feature:1')

    def test_file(self):
        yield from self._testFile(('features', 'normal.feature'))
        self.assertLastCommand('cucumber features/normal.feature')

    def test_suite(self):
        yield from self._testSuite(('features', 'normal.feature'))
        self.assertLastCommand('cucumber')
