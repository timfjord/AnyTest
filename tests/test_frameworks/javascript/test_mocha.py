from AnyTest.tests import SublimeProjectTestCase


class MochaJavaScriptTestCase(SublimeProjectTestCase):
    folder = ("mocha", "javascript")

    def test_line(self):
        yield from self._testFile(("test", "normal.js"), 2)
        self.assertLastCommand("mocha ", ("test", "normal.js"), " --grep '^Math'")

        self._testLine(3)
        self.assertLastCommand(
            "mocha ", ("test", "normal.js"), " --grep '^Math Addition'"
        )

        self._testLine(4)
        self.assertLastCommand(
            "mocha ",
            ("test", "normal.js"),
            " --grep '^Math Addition adds two numbers$'",
        )

    def test_line_context(self):
        yield from self._testFile(("test", "context.js"), 1)
        self.assertLastCommand("mocha ", ("test", "context.js"), " --grep '^Math'")

        self._testLine(2)
        self.assertLastCommand(
            "mocha ", ("test", "context.js"), " --grep '^Math Addition'"
        )

        self._testLine(3)
        self.assertLastCommand(
            "mocha ",
            ("test", "context.js"),
            " --grep '^Math Addition adds two numbers$'",
        )

    def test_list_coffee(self):
        yield from self._testFile(("test", "normal.coffee"), 1)
        self.assertLastCommand("mocha ", ("test", "normal.coffee"), " --grep '^Math'")

        self._testLine(2)
        self.assertLastCommand(
            "mocha ", ("test", "normal.coffee"), " --grep '^Math Addition'"
        )

        self._testLine(3)
        self.assertLastCommand(
            "mocha ",
            ("test", "normal.coffee"),
            " --grep '^Math Addition adds two numbers$'",
        )

    def test_line_react(self):
        yield from self._testFile(("test", "normal.jsx"), 1)
        self.assertLastCommand("mocha ", ("test", "normal.jsx"), " --grep '^Math'")

        self._testLine(2)
        self.assertLastCommand(
            "mocha ", ("test", "normal.jsx"), " --grep '^Math Addition'"
        )

        self._testLine(3)
        self.assertLastCommand(
            "mocha ",
            ("test", "normal.jsx"),
            " --grep '^Math Addition adds two numbers$'",
        )

    def test_line_typescript(self):
        yield from self._testFile(("test", "normal.ts"), 1)
        self.assertLastCommand("mocha ", ("test", "normal.ts"), " --grep '^Math'")

        self._testLine(2)
        self.assertLastCommand(
            "mocha ", ("test", "normal.ts"), " --grep '^Math Addition'"
        )

        self._testLine(3)
        self.assertLastCommand(
            "mocha ",
            ("test", "normal.ts"),
            " --grep '^Math Addition adds two numbers$'",
        )

    def test_line_typescript_jsx(self):
        yield from self._testFile(("test", "normal.tsx"), 1)
        self.assertLastCommand("mocha ", ("test", "normal.tsx"), " --grep '^Math'")

        self._testLine(2)
        self.assertLastCommand(
            "mocha ", ("test", "normal.tsx"), " --grep '^Math Addition'"
        )

        self._testLine(3)
        self.assertLastCommand(
            "mocha ",
            ("test", "normal.tsx"),
            " --grep '^Math Addition adds two numbers$'",
        )

    def test_line_no_nearest(self):
        yield from self._testFile(("test", "normal.js"), 1)
        self.assertLastCommand("mocha ", ("test", "normal.js"))

    def test_file(self):
        yield from self._testFile(("test", "normal.js"))
        self.assertLastCommand("mocha ", ("test", "normal.js"))

    def test_file_outside_test_folder(self):
        yield from self._testFile(("src", "addition.test.js"))
        self.assertLastCommand("mocha ", ("src", "addition.test.js"))

    def test_suite(self):
        yield from self._testSuite(("test", "normal.js"))
        self.assertLastCommand("mocha --recursive test/")

    def test_suite_tests_dir(self):
        yield from self._testSuite(("tests", "normal.js"))
        self.assertLastCommand("mocha --recursive tests/")

    def test_suite_outisde_test_folder(self):
        yield from self._testSuite(("src", "addition.test.js"))
        self.assertLastCommand("mocha ", ('"src', "**", '*.test.js"'))


class MochaTypeScriptTestCase(SublimeProjectTestCase):
    folder = ("mocha", "typescript")
    settings = {"javascript.test_framework": "mocha"}

    def test_line(self):
        yield from self._testFile(("test", "normal.ts"), 2)
        self.assertLastCommand(
            "mocha -r ",
            ("ts-node", "register"),
            " ",
            ("test", "normal.ts"),
            " --grep '^Math'",
        )

        self._testLine(3)
        self.assertLastCommand(
            "mocha -r ",
            ("ts-node", "register"),
            " ",
            ("test", "normal.ts"),
            " --grep '^Math Addition'",
        )

        self._testLine(4)
        self.assertLastCommand(
            "mocha -r ",
            ("ts-node", "register"),
            " ",
            ("test", "normal.ts"),
            " --grep '^Math Addition adds two numbers$'",
        )

    def test_line_jsx(self):
        yield from self._testFile(("test", "normal.tsx"), 1)
        self.assertLastCommand(
            "mocha -r ",
            ("ts-node", "register"),
            " ",
            ("test", "normal.tsx"),
            " --grep '^Math'",
        )

        self._testLine(2)
        self.assertLastCommand(
            "mocha -r ",
            ("ts-node", "register"),
            " ",
            ("test", "normal.tsx"),
            " --grep '^Math Addition'",
        )

        self._testLine(3)
        self.assertLastCommand(
            "mocha -r ",
            ("ts-node", "register"),
            " ",
            ("test", "normal.tsx"),
            " --grep '^Math Addition adds two numbers$'",
        )

    def test_line_no_nearest(self):
        yield from self._testFile(("test", "normal.ts"), 1)
        self.assertLastCommand(
            "mocha -r ", ("ts-node", "register"), " ", ("test", "normal.ts")
        )

    def test_file(self):
        yield from self._testFile(("test", "normal.ts"))
        self.assertLastCommand(
            "mocha -r ", ("ts-node", "register"), " ", ("test", "normal.ts")
        )

    def test_file_outside_test_folder(self):
        yield from self._testFile(("src", "addition.test.ts"))
        self.assertLastCommand(
            "mocha -r ", ("ts-node", "register"), " ", ("src", "addition.test.ts")
        )

    def test_suite(self):
        yield from self._testSuite(("test", "normal.ts"))
        self.assertLastCommand(
            "mocha -r ", ("ts-node", "register"), " --recursive test/ --extension ts"
        )

    def test_suite_tests_dir(self):
        yield from self._testSuite(("tests", "normal.ts"))
        self.assertLastCommand(
            "mocha -r ", ("ts-node", "register"), " --recursive tests/ --extension ts"
        )

    def test_suite_outisde_test_folder(self):
        yield from self._testSuite(("src", "addition.test.ts"))
        self.assertLastCommand(
            "mocha -r ", ("ts-node", "register"), " ", ('"src', "**", '*.test.ts"')
        )
