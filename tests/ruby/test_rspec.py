from AnyTest.tests import SublimeViewTestCase


class RspecTestCase(SublimeViewTestCase):
    def setUp(self):
        super().setUp()

        self.openFolder('rspec')

    def test_line1(self):
        yield from self._testFile('normal_spec.rb', 1)
        self.assertLastCommand('rspec normal_spec.rb:1')

    def test_line2(self):
        yield from self._testFile('context_spec.rb', 1)
        self.assertLastCommand('rspec context_spec.rb:1')

        self._testLine(2)
        self.assertLastCommand('rspec context_spec.rb:2')

        self._testLine(line=3)
        self.assertLastCommand('rspec context_spec.rb:3')

    def test_file(self):
        yield from self._testFile('normal_spec.rb')
        self.assertLastCommand('rspec normal_spec.rb')

    def test_suite(self):
        yield from self._testSuite('normal_spec.rb')
        self.assertLastCommand('rspec')

    def test_turnip(self):
        yield from self._testFile('math.feature')

        self.assertLastCommand('rspec math.feature')
