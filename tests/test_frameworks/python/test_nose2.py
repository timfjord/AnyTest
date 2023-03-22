from AnyTest.tests import SublimeProjectTestCase


class Nose2TestCase(SublimeProjectTestCase):
    folder = "nose"
    settings = {"python.test_framework": "nose2"}

    def test_line(self):
        yield from self._testFile("test_class.py", 2)
        self.assertLastCommand("nose2 test_class.TestNumbers.test_numbers")

        self._testLine(5)
        self.assertLastCommand("nose2 test_class.TestSubclass")

        self._testLine(1)
        self.assertLastCommand("nose2 test_class.TestNumbers")

        yield from self._testFile("test_method.py", 4)
        self.assertLastCommand("nose2 test_method.test_numbers")

    def test_line_no_nearest(self):
        yield from self._testFile("test_method.py", 1)
        self.assertLastCommand("nose2 test_method")

    def test_file(self):
        yield from self._testFile("test_class.py")
        self.assertLastCommand("nose2 test_class")

    def test_suite(self):
        yield from self._testSuite("test_class.py")
        self.assertLastCommand("nose2")
