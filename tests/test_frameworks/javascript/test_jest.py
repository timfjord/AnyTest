from AnyTest.tests import SublimeProjectTestCase


class JestTestCase(SublimeProjectTestCase):
    folder = "jest"

    def test_line(self):
        yield from self._testFile(("__tests__", "normal-test.js"), 2)
        self.assertLastCommand(
            "jest --no-coverage -t '^Math' -- ", ("__tests__", "normal-test.js")
        )

        self._testLine(3)
        self.assertLastCommand(
            "jest --no-coverage -t '^Math Addition' -- ",
            ("__tests__", "normal-test.js"),
        )

        self._testLine(4)
        self.assertLastCommand(
            "jest --no-coverage -t '^Math Addition adds two numbers$' -- ",
            ("__tests__", "normal-test.js"),
        )

    def test_line_context(self):
        yield from self._testFile(("__tests__", "context-test.js"), 1)
        self.assertLastCommand(
            "jest --no-coverage -t '^Math' -- ", ("__tests__", "context-test.js")
        )

        self._testLine(2)
        self.assertLastCommand(
            "jest --no-coverage -t '^Math Addition' -- ",
            ("__tests__", "context-test.js"),
        )

        self._testLine(3)
        self.assertLastCommand(
            "jest --no-coverage -t '^Math Addition adds two numbers$' -- ",
            ("__tests__", "context-test.js"),
        )

    def test_line_coffee(self):
        yield from self._testFile(("__tests__", "normal-test.coffee"), 1)
        self.assertLastCommand(
            "jest --no-coverage -t '^Math' -- ", ("__tests__", "normal-test.coffee")
        )

        self._testLine(2)
        self.assertLastCommand(
            "jest --no-coverage -t '^Math Addition' -- ",
            ("__tests__", "normal-test.coffee"),
        )

        self._testLine(3)
        self.assertLastCommand(
            "jest --no-coverage -t '^Math Addition adds two numbers$' -- ",
            ("__tests__", "normal-test.coffee"),
        )

    def test_line_react(self):
        yield from self._testFile(("__tests__", "normal-test.jsx"), 1)
        self.assertLastCommand(
            "jest --no-coverage -t '^Math' -- ", ("__tests__", "normal-test.jsx")
        )

        self._testLine(2)
        self.assertLastCommand(
            "jest --no-coverage -t '^Math Addition' -- ",
            ("__tests__", "normal-test.jsx"),
        )

        self._testLine(3)
        self.assertLastCommand(
            "jest --no-coverage -t '^Math Addition adds two numbers$' -- ",
            ("__tests__", "normal-test.jsx"),
        )

    def test_line_no_nearest(self):
        yield from self._testFile(("__tests__", "normal-test.js"), 1)
        self.assertLastCommand(
            "jest --no-coverage -- ", ("__tests__", "normal-test.js")
        )

    def test_file(self):
        yield from self._testFile(("__tests__", "normal-test.js"))
        self.assertLastCommand(
            "jest --no-coverage -- ", ("__tests__", "normal-test.js")
        )

    def test_file_outside_tests_folder(self):
        yield from self._testFile("outside-test.js")
        self.assertLastCommand("jest --no-coverage -- outside-test.js")

    def test_suite(self):
        yield from self._testSuite(("__tests__", "normal-test.js"))
        self.assertLastCommand("jest --no-coverage")


class NpmRunJestTestCase(SublimeProjectTestCase):
    folder = "jest"
    settings = {"javascript.jest.executable": ["npm", "run", "jest"]}

    def test_file(self):
        yield from self._testFile(("__tests__", "normal-test.js"))
        self.assertLastCommand(
            "npm run jest --no-coverage -- ", ("__tests__", "normal-test.js")
        )


class YarnJestTestCase(SublimeProjectTestCase):
    folder = "jest"
    settings = {"javascript.jest.executable": ["yarn", "jest"]}

    def test_no_end_of_options(self):
        yield from self._testFile(("__tests__", "normal-test.js"))
        self.assertLastCommand(
            "yarn jest --no-coverage ", ("__tests__", "normal-test.js")
        )


class LocalYarnJestTestCase(SublimeProjectTestCase):
    folder = "jest"
    settings = {"javascript.jest.executable": ["~/.local/bin/yarn", "jest"]}

    def test_no_end_of_options(self):
        yield from self._testFile(("__tests__", "normal-test.js"))
        self.assertLastCommand(
            "~/.local/bin/yarn jest --no-coverage ", ("__tests__", "normal-test.js")
        )
