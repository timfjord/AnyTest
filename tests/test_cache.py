import unittest
from unittest.mock import patch

from AnyTest.plugin import cache


class CacheTestCase(unittest.TestCase):
    def _inner_method(self):
        return "something"

    @cache.cache
    def cached_method(self):
        return self._inner_method()

    def test_cache(self):
        with patch.object(self, "_inner_method") as mock:
            for _ in range(3):
                self.cached_method()

        self.assertEqual(mock.call_count, 1)

    def test_clear_cache(self):
        with patch.object(self, "_inner_method") as mock:
            for _ in range(3):
                cache.clear()
                self.cached_method()

        self.assertEqual(mock.call_count, 3)
