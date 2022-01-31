from AnyTest.tests import SublimeViewTestCase


class WithoutMixTestCase(SublimeViewTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.openFolder('exunit')

    def test_line(self):
        yield from self._testFile('normal_test.exs', 6)
        self.assertLastCommand('elixir normal_test.exs')

    def test_file(self):
        yield from self._testFile('normal_test.exs')
        self.assertLastCommand('elixir normal_test.exs')

    def test_suite(self):
        yield from self._testSuite('normal_test.exs')
        self.assertLastCommand('elixir *.exs')


class MixTestCase(SublimeViewTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.openFolder('exunit', 'mix')

    def test_first_line(self):
        yield from self._testFile('normal_test.exs', 1)
        self.assertLastCommand('mix test normal_test.exs')

    def test_specific_line(self):
        yield from self._testFile('normal_test.exs', 6)
        self.assertLastCommand('mix test normal_test.exs:6')

    def test_file(self):
        yield from self._testFile('normal_test.exs')
        self.assertLastCommand('mix test normal_test.exs')

    def test_suite(self):
        yield from self._testSuite('normal_test.exs')
        self.assertLastCommand('mix test')
