class TestNumbers:
    def test_numbers(self):
        assert 1 == 1


class TestSubclass(TestCase):  # noqa
    def test_numbers(self):
        assert 1 == 1


class Test_underscores_and_123(TestCase):  # noqa
    def test_underscores(self):
        assert 1 == 1


class TestNestedClass:
    def test_nested(self):
        class NestedClass:
            ...

        assert 1 == 1
