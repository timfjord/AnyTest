from AnyTest.tests import SublimeProjectTestCase


class MTestCase(SublimeProjectTestCase):
    folder = ('minitest', 'rake')
    settings = {'ruby.minitest.use_m': True}

    def test_line(self):
        yield from self._testFile('classic_unit_test.rb', 3)
        self.assertLastCommand('m classic_unit_test.rb:3')

    def test_file(self):
        yield from self._testFile('classic_unit_test.rb')
        self.assertLastCommand('m classic_unit_test.rb')

    def test_suite(self):
        yield from self._testSuite('classic_unit_test.rb')
        self.assertLastCommand('m')
