from AnyTest.tests import SublimeProjectTestCase


class BehaveTestCase(SublimeProjectTestCase):
    folder = "behave"

    def test_line(self):
        yield from self._testFile(("features", "test.feature"), 5)
        self.assertLastCommand("behave ", ("features", "test.feature"), ":5")

    def test_file(self):
        yield from self._testFile(("features", "test.feature"))
        self.assertLastCommand("behave ", ("features", "test.feature"), "")

    def test_suite(self):
        yield from self._testSuite(("features", "test.feature"))
        self.assertLastCommand("behave")
