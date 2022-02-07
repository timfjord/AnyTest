from unittest.mock import patch

from AnyTest.tests import SublimeProjectTestCase


class PytestTestCase(SublimeProjectTestCase):
    folder = 'pytest'
    settings = {
        'python.test_framework': 'pytest',
        'python.pytest.executable': ['pytest'],
    }

    def test_line(self):
        yield from self._testFile('test_class.py', 1)
        self.assertLastCommand('pytest test_class.py::TestClass')

        self._testLine(2)
        self.assertLastCommand('pytest test_class.py::TestClass::TestNestedClass')

        self._testLine(3)
        self.assertLastCommand(
            'pytest test_class.py::TestClass::TestNestedClass::test_nestedclass_method'
        )

        self._testLine(6)
        self.assertLastCommand('pytest test_class.py::TestClass::test_method')

        self._testLine(10)
        self.assertLastCommand('pytest test_class.py::test_function')


class PytestXunitTestCase(SublimeProjectTestCase):
    folder = 'nose'
    settings = {
        'python.test_framework': 'pytest',
        'python.pytest.executable': ['pytest'],
    }

    def test_line(self):
        yield from self._testFile('test_class.py', 1)
        self.assertLastCommand('pytest test_class.py::TestNumbers')

        self._testLine(2)
        self.assertLastCommand('pytest test_class.py::TestNumbers::test_numbers')

        self._testLine(8)
        self.assertLastCommand('pytest test_class.py::TestSubclass::test_subclass')

        self._testLine(11)
        self.assertLastCommand('pytest test_class.py::Test_underscores_and_123')

        self._testLine(13)
        self.assertLastCommand(
            'pytest test_class.py::Test_underscores_and_123::test_underscores'
        )

        self._testLine(16)
        self.assertLastCommand('pytest test_class.py::UnittestClass')

        self._testLine(22)
        self.assertLastCommand('pytest test_class.py::SomeTest::test_foo')

        yield from self._testFile('test_method.py', 4)
        self.assertLastCommand('pytest test_method.py::test_numbers')

    def test_line_no_nearest(self):
        yield from self._testFile('test_method.py', 1)

        self.assertLastCommand('pytest test_method.py')

    def test_file(self):
        yield from self._testFile('test_class.py')

        self.assertLastCommand('pytest test_class.py')

    def test_suite(self):
        yield from self._testSuite('test_class.py')

        self.assertLastCommand('pytest')


class PipenvPytestTestCase(SublimeProjectTestCase):
    folder = 'pipenv'
    settings = {'python.test_framework': 'pytest'}

    def test_line(self):
        # I couldn't make it working with a class decorator or start/stop
        with patch(
            'AnyTest.plugin.test_frameworks.utils.is_executable', return_value=False
        ):
            yield from self._testFile('test_class.py', 1)
            self.assertLastCommand(
                'pipenv run python -m pytest test_class.py::TestNumbers'
            )

    def test_file(self):
        with patch(
            'AnyTest.plugin.test_frameworks.utils.is_executable', return_value=False
        ):
            yield from self._testFile('test_class.py')
            self.assertLastCommand('pipenv run python -m pytest test_class.py')

    def test_suite(self):
        with patch(
            'AnyTest.plugin.test_frameworks.utils.is_executable', return_value=False
        ):
            yield from self._testSuite('test_class.py')
            self.assertLastCommand('pipenv run python -m pytest')


class PoetryPytestTestCase(SublimeProjectTestCase):
    folder = 'poetry'
    settings = {'python.test_framework': 'pytest'}

    def test_line(self):
        with patch(
            'AnyTest.plugin.test_frameworks.utils.is_executable', return_value=False
        ):
            yield from self._testFile('test_class.py', 1)
            self.assertLastCommand(
                'poetry run python -m pytest test_class.py::TestNumbers'
            )

    def test_file(self):
        with patch(
            'AnyTest.plugin.test_frameworks.utils.is_executable', return_value=False
        ):
            yield from self._testFile('test_class.py')
            self.assertLastCommand('poetry run python -m pytest test_class.py')

    def test_suite(self):
        with patch(
            'AnyTest.plugin.test_frameworks.utils.is_executable', return_value=False
        ):
            yield from self._testSuite('test_class.py')
            self.assertLastCommand('poetry run python -m pytest')
