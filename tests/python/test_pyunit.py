from AnyTest.tests import SublimeProjectTestCase


class PyunitTestCase(SublimeProjectTestCase):
    folder = 'pyunit'

    def setUp(self):
        super().setUp()

        self.setSettings({'python.test_framework': 'pyunit'})

    def test_line(self):
        yield from self._testFile(('module', 'test_class.py'), 2)
        self.assertLastCommand(
            'python -m unittest module.test_class.TestNumbers.test_numbers'
        )

        yield from self._testFile(('module', 'test_class.py'), 6)
        self.assertLastCommand('python -m unittest module.test_class.TestSubclass')

        self._testLine(1)
        self.assertLastCommand('python -m unittest module.test_class.TestNumbers')

        self._testLine(18)
        self.assertLastCommand(
            'python -m unittest module.test_class.TestNestedClass.test_nested'
        )

        yield from self._testFile(('module', 'test_method.py'), 4)
        self.assertLastCommand('python -m unittest module.test_method.test_numbers')

    def test_line_no_nearest(self):
        yield from self._testFile(('module', 'test_method.py'), 1)
        self.assertLastCommand('python -m unittest module.test_method')

    def test_file(self):
        yield from self._testFile(('module', 'test_method.py'))
        self.assertLastCommand('python -m unittest module.test_method')

    def test_suite(self):
        yield from self._testSuite(('module', 'test_class.py'))
        self.assertLastCommand('python -m unittest')