from AnyTest.tests import SublimeProjectTestCase


class RailsTestCase(SublimeProjectTestCase):
    folder = "rails"

    def test_line(self):
        yield from self._testFile("normal_test.rb", 11)
        self.assertLastCommand("rails test normal_test.rb:11")

    def test_file(self):
        yield from self._testFile("normal_test.rb")
        self.assertLastCommand("rails test normal_test.rb")

    def test_suite(self):
        yield from self._testSuite("normal_test.rb")
        self.assertLastCommand("rails test")


class RailsEngineTestCase(RailsTestCase):
    folder = ("rails", "engine")
