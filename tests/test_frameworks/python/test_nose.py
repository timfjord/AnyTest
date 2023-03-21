from AnyTest.tests import SublimeProjectTestCase


class NoseTestCase(SublimeProjectTestCase):
    folder = "nose"
    settings = {"python.test_framework": "nose"}

    def test_line(self):
        yield from self._testFile("test_class.py", 2)
        self.assertLastCommand(
            "nosetests --doctest-tests test_class.py:TestNumbers.test_numbers"
        )

        self._testLine(5)
        self.assertLastCommand("nosetests --doctest-tests test_class.py:TestSubclass")

        self._testLine(1)
        self.assertLastCommand("nosetests --doctest-tests test_class.py:TestNumbers")

        yield from self._testFile("test_method.py", 4)
        self.assertLastCommand("nosetests --doctest-tests test_method.py:test_numbers")

    def test_line_no_nearest(self):
        yield from self._testFile("test_method.py", 1)
        self.assertLastCommand("nosetests --doctest-tests test_method.py")

    def test_file(self):
        yield from self._testFile("test_class.py")
        self.assertLastCommand("nosetests --doctest-tests test_class.py")

    def test_suite(self):
        yield from self._testSuite("test_class.py")
        self.assertLastCommand("nosetests --doctest-tests")


class NosePipenvTestCase(SublimeProjectTestCase):
    folder = "pipenv"
    settings = {"python.test_framework": "nose"}

    def test_line(self):
        yield from self._testFile("test_class.py", 1)
        self.assertLastCommand(
            "pipenv run nosetests --doctest-tests test_class.py:TestNumbers"
        )

    def test_file(self):
        yield from self._testFile("test_class.py")
        self.assertLastCommand("pipenv run nosetests --doctest-tests test_class.py")

    def test_suite(self):
        yield from self._testSuite("test_class.py")
        self.assertLastCommand("pipenv run nosetests --doctest-tests")


class NosePoetryTestCase(SublimeProjectTestCase):
    folder = "poetry"
    settings = {"python.test_framework": "nose"}

    def test_line(self):
        yield from self._testFile("test_class.py", 1)
        self.assertLastCommand(
            "poetry run nosetests --doctest-tests test_class.py:TestNumbers"
        )

    def test_file(self):
        yield from self._testFile("test_class.py")
        self.assertLastCommand("poetry run nosetests --doctest-tests test_class.py")

    def test_suite(self):
        yield from self._testSuite("test_class.py")
        self.assertLastCommand("poetry run nosetests --doctest-tests")


class NosePdmTestCase(SublimeProjectTestCase):
    folder = "pdm"
    settings = {"python.test_framework": "nose"}

    def test_line(self):
        yield from self._testFile("test_class.py", 1)
        self.assertLastCommand(
            "pdm run nosetests --doctest-tests test_class.py:TestNumbers"
        )

    def test_file(self):
        yield from self._testFile("test_class.py")
        self.assertLastCommand("pdm run nosetests --doctest-tests test_class.py")

    def test_suite(self):
        yield from self._testSuite("test_class.py")
        self.assertLastCommand("pdm run nosetests --doctest-tests")
