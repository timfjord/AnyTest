class TestNumbers:
    def test_numbers(self):
        assert 1 == 1


class TestSubclass(Subclass):  # noqa
    def test_subclass(self):
        assert 1 == 1


class Test_underscores_and_123(Subclass):  # noqa
    def test_underscores(self):
        assert 1 == 1


class UnittestClass(unittest.TestCase):  # noqa
    def test_unittest(self):
        assert 1 == 1


class SomeTest(TestCase):  # noqa
    def test_foo(self):
        foo = date(2017, 11, 16)  # noqa
