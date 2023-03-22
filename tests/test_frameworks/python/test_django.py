from AnyTest.tests import SublimeProjectTestCase


class DjangoTestCase(SublimeProjectTestCase):
    folder = "django"
    settings = {"python.test_framework": "django"}

    def test_line(self):
        yield from self._testFile(("module", "test_class.py"), 2)
        self.assertLastCommand(
            "python manage.py test module.test_class.TestNumbers.test_numbers"
        )

        self._testLine(5)
        self.assertLastCommand("python manage.py test module.test_class.TestSubclass")

        self._testLine(1)
        self.assertLastCommand("python manage.py test module.test_class.TestNumbers")

        yield from self._testFile(("module", "test_method.py"), 4)
        self.assertLastCommand("python manage.py test module.test_method.test_numbers")

    def test_line_no_nearest(self):
        yield from self._testFile(("module", "test_method.py"), 1)
        self.assertLastCommand("python manage.py test module.test_method")

    def test_file(self):
        yield from self._testFile(("module", "test_class.py"))
        self.assertLastCommand("python manage.py test module.test_class")

    def test_suite(self):
        yield from self._testSuite("test_class.py")
        self.assertLastCommand("python manage.py test")


class DjangoNoseTestCase(SublimeProjectTestCase):
    folder = "django"
    settings = {"python.test_framework": "django", "python.django.use_nose": True}

    def test_line(self):
        yield from self._testFile(("module", "test_class.py"), 2)
        self.assertLastCommand(
            "python manage.py test module.test_class:TestNumbers.test_numbers"
        )
