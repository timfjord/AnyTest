from AnyTest.tests import SublimeProjectTestCase


class TestBenchTestCase(SublimeProjectTestCase):
    folder = "test_bench"

    def test_line(self):
        yield from self._testFile(("test", "automated", "math.rb"), 1)
        self.assertLastCommand("bundle exec bench ", ("test", "automated", "math.rb"))

    def test_file(self):
        yield from self._testFile(("test", "automated", "math.rb"))
        self.assertLastCommand("bundle exec bench ", ("test", "automated", "math.rb"))

    def test_suite(self):
        yield from self._testSuite(("test", "automated", "math.rb"))
        self.assertLastCommand("bundle exec bench ", ("test", "automated", ""))
