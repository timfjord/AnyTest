from AnyTest.tests import SublimeProjectTestCase


class MambaTestCase(SublimeProjectTestCase):
    folder = "mamba"
    settings = {
        "python.test_framework": "mamba",
        "python.pytest.executable": ["mamba"],
    }

    def test_line(self):
        yield from self._testFile("normal_spec.py", 6)
        self.assertLastCommand("mamba normal_spec.py")

    def test_file(self):
        yield from self._testFile("normal_spec.py")
        self.assertLastCommand("mamba normal_spec.py")

    def test_suite(self):
        yield from self._testSuite("normal_spec.py")
        self.assertLastCommand("mamba")
