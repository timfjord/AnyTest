from AnyTest.tests import SublimeProjectTestCase


class EspecTestCase(SublimeProjectTestCase):
    folder = "espec"

    def test_line(self):
        yield from self._testFile("normal_spec.exs", 3)
        self.assertLastCommand("mix espec normal_spec.exs:3")

    def test_file(self):
        yield from self._testFile("normal_spec.exs")
        self.assertLastCommand("mix espec normal_spec.exs")

    def test_suite(self):
        yield from self._testSuite("normal_spec.exs")
        self.assertLastCommand("mix espec")
