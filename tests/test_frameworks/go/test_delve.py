from AnyTest.tests import SublimeProjectTestCase


class GotestTestCase(SublimeProjectTestCase):
    folder = 'delve'
    settings = {'go.test_framework': 'delve'}

    def test_line_gotest(self):
        yield from self._testFile('normal_test.go', 5)
        self.assertLastCommand('dlv test ./. -- -test.run \'TestNumbers$\'')

        self._testLine(9)
        self.assertLastCommand('dlv test ./. -- -test.run \'Testテスト$\'')

        self._testLine(13)
        self.assertLastCommand('dlv test ./. -- -test.run \'ExampleSomething$\'')

    def test_line_ginkgo(self):
        yield from self._testFile('ginkgo_test.go', 17)
        self.assertLastCommand(
            'dlv test ./. -- -ginkgo.focus=\'should paginate the result\''
        )

    def test_line_subdirectory(self):
        yield from self._testFile(('mypackage', 'normal_test.go'), 5)
        self.assertLastCommand('dlv test ./mypackage -- -test.run \'TestNumbers$\'')

        self._testLine(9)
        self.assertLastCommand('dlv test ./mypackage -- -test.run \'Testテスト$\'')

        self._testLine(13)
        self.assertLastCommand(
            'dlv test ./mypackage -- -test.run \'ExampleSomething$\''
        )

    def test_line_no_nearest(self):
        yield from self._testFile('normal_test.go', 1)
        self.assertLastCommand('dlv test')

    def test_file(self):
        yield from self._testFile('normal_test.go')
        self.assertLastCommand('dlv test')

    def test_file_subdirectory(self):
        yield from self._testFile('mypackage/normal_test.go')
        self.assertLastCommand('dlv test ./mypackage/...')

    def test_suite(self):
        yield from self._testSuite('normal_test.go')
        self.assertLastCommand('dlv test ./...')
