from AnyTest.tests import SublimeProjectTestCase


class GotestTestCase(SublimeProjectTestCase):
    folder = "gotest"
    settings = {"go.test_framework": "gotest"}

    def test_line(self):
        yield from self._testFile("normal_test.go", 5)
        self.assertLastCommand("go test -run TestNumbers$ ./.")

        self._testLine(8)
        self.assertLastCommand("go test -run TestNumbers/adding_two_numbers$ ./.")

        self._testLine(12)
        self.assertLastCommand(
            r"go test -run TestNumbers/\\\[\\\]\\\.\\\*\\\+\\\?\\\|\\\$\\\^\\\(\\\)$ ./."
        )

        self._testLine(17)
        self.assertLastCommand("go test -run TestNumbers/this_is/nested$ ./.")

        self._testLine(23)
        self.assertLastCommand("go test -run Testテスト$ ./.")

        self._testLine(27)
        self.assertLastCommand("go test -run ExampleSomething$ ./.")

        self._testLine(36)
        self.assertLastCommand("go test -run TestSomethingInASuite$ ./.")

    def test_line_subdirectory(self):
        yield from self._testFile(("mypackage", "normal_test.go"), 5)
        self.assertLastCommand("go test -run TestNumbers$ ./mypackage")

        self._testLine(9)
        self.assertLastCommand("go test -run Testテスト$ ./mypackage")

        self._testLine(13)
        self.assertLastCommand("go test -run ExampleSomething$ ./mypackage")

        self._testLine(22)
        self.assertLastCommand("go test -run TestSomething$ ./mypackage")

    def test_line_build_tags(self):
        yield from self._testFile("build_tags_test.go", 14)
        self.assertLastCommand(
            "go test -run TestNumbers$ -tags=foo,hello,world,!bar,red,black ./."
        )

    def test_file(self):
        yield from self._testFile("normal_test.go")
        self.assertLastCommand("go test")

    def test_file_subdirectory(self):
        yield from self._testFile("mypackage/normal_test.go")
        self.assertLastCommand("go test ./mypackage/...")

    def test_file_build_tags(self):
        yield from self._testFile("build_tags_test.go")
        self.assertLastCommand("go test -tags=foo,hello,world,!bar,red,black")

    def test_suite(self):
        yield from self._testSuite("normal_test.go")
        self.assertLastCommand("go test ./...")

    def test_suite_build_tags(self):
        yield from self._testSuite("build_tags_test.go")
        self.assertLastCommand("go test ./...")
