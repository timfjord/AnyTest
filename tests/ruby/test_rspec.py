from AnyTest.tests import SublimeViewTestCase
from AnyTest.plugin.test_frameworks import TestFramework


class RspecTestCase(SublimeViewTestCase):
    def test_nearest1(self):
        yield from self._testFile('rspec', 'normal_spec.rb', 1)
        self.assertLastCommand('rspec normal_spec.rb:1')

    def test_nearest2(self):
        yield from self._testFile('rspec', 'context_spec.rb', 1)
        self.assertLastCommand('rspec context_spec.rb:1')

        self._testLine(2)
        self.assertLastCommand('rspec context_spec.rb:2')

        self._testLine(line=3)
        self.assertLastCommand('rspec context_spec.rb:3')

    def test_file(self):
        yield from self._testFile('rspec', 'normal_spec.rb')
        self.assertLastCommand('rspec normal_spec.rb')

    def test_suite(self):
        yield from self._testFile(
            'rspec', 'normal_spec.rb', scope=TestFramework.SCOPE_SUITE
        )
        self.assertLastCommand('rspec')

    def test_turnip(self):
        yield from self._testFile('rspec', 'math.feature')

        self.assertLastCommand('rspec math.feature')
