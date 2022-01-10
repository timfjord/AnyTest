from AnyTest.tests import SublimeViewTestCase
from AnyTest.plugin.test_frameworks import TestFramework


class WithoutMixTestCase(SublimeViewTestCase):
    def test_line(self):
        yield from self._testFile('exunit', 'normal_test.exs', 6)
        self.assertLastCommand('elixir normal_test.exs')

    def test_file(self):
        yield from self._testFile('exunit', 'normal_test.exs')
        self.assertLastCommand('elixir normal_test.exs')

    def test_suite(self):
        yield from self._testFile(
            'exunit', 'normal_test.exs', scope=TestFramework.SCOPE_SUITE
        )
        self.assertLastCommand('elixir *.exs')


class MixTestCase(SublimeViewTestCase):
    def test_first_line(self):
        yield from self._testFile(('exunit', 'mix'), 'normal_test.exs', 1)
        self.assertLastCommand('mix test normal_test.exs')

    def test_specific_line(self):
        yield from self._testFile(('exunit', 'mix'), 'normal_test.exs', 6)
        self.assertLastCommand('mix test normal_test.exs:6')

    def test_file(self):
        yield from self._testFile(('exunit', 'mix'), 'normal_test.exs')
        self.assertLastCommand('mix test normal_test.exs')

    def test_suite(self):
        yield from self._testFile(
            ('exunit', 'mix'), 'normal_test.exs', scope=TestFramework.SCOPE_SUITE
        )
        self.assertLastCommand('mix test')
