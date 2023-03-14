import unittest

from AnyTest.plugin.utils import escape_regex, replace


class UtilsTestCase(unittest.TestCase):
    def test_escape_regex(self):
        self.assertEqual(
            escape_regex("?+*\\^$.|{}[]()"), r"\?\+\*\\\^\$\.\|\{\}\[\]\(\)"
        )
        self.assertEqual(escape_regex("/"), "/")

    def test_replace(self):
        self.assertEqual(
            replace("foo-bar_baz/qux", ("-", "_"), ("/", "_")),
            "foo_bar_baz_qux",
        )
