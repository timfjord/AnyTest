from AnyTest.tests import SublimeProjectTestCase


class ZigtestTestCase(SublimeProjectTestCase):
    folder = "zigtest"

    def test_line(self):
        yield from self._testFile("normal.zig", 9)
        self.assertLastCommand("zig test normal.zig --test-filter 'numbers 2'")

    def test_file(self):
        yield from self._testFile("normal.zig")
        self.assertLastCommand("zig test normal.zig")

    def test_suite(self):
        yield from self._testSuite("normal.zig")
        self.assertLastCommand("zig build test")
