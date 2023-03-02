from AnyTest.tests import SublimeProjectTestCase


class GoTestTestCase(SublimeProjectTestCase):
    folder = 'gotest'

    def test_line(self):
        yield from self._testFile('normal_test.go', 5)
        self.assertLastCommand('go test -run TestNumbers$ ./.')

        self._testLine(8)
        self.assertLastCommand('go test -run TestNumbers/adding_two_numbers$ ./.')

        self._testLine(12)
        self.assertLastCommand(
            r'go test -run TestNumbers/\\\[\\\]\\\.\\\*\\\+\\\?\\\|\\\$\\\^\\\(\\\)$ ./.'
        )

        self._testLine(17)
        self.assertLastCommand('go test -run TestNumbers/this_is/nested$ ./.')

        self._testLine(23)
        self.assertLastCommand('go test -run Testテスト$ ./.')

        self._testLine(27)
        self.assertLastCommand('go test -run ExampleSomething$ ./.')

        self._testLine(36)
        self.assertLastCommand('go test -run TestSomethingInASuite$ ./.')

    def test_file(self):
        yield from self._testFile('normal_test.go')
        self.assertLastCommand('go test')

    def test_file_subdirectory(self):
        yield from self._testFile('mypackage/normal_test.go')
        self.assertLastCommand('go test ./mypackage/...')

    def test_suite(self):
        yield from self._testSuite('normal_test.go')
        self.assertLastCommand('go test ./...')
