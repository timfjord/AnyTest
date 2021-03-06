from unittest.mock import patch

from AnyTest.plugin.context import Context
from AnyTest.tests import SublimeViewTestCase


class ContextTestCase(SublimeViewTestCase):
    def setUp(self):
        super().setUp()

        self.view.run_command(
            "insert",
            {
                "characters": "line1\nline2\nline3\nline4\nline5\nline6\nline7\nline8\nline9"
            },
        )
        with patch('AnyTest.plugin.context.Root.find', return_value=('root', 'file')):
            self.context = Context(self.view)

    def test_get_line(self):
        self.assertEqual(self.context.get_line(0), 1)

    def test_get_lines_no_args(self):
        self.gotoLine(1)
        self.assertEqual(
            list(self.context.lines()),
            [
                ('line1', 1),
                ('line2', 2),
                ('line3', 3),
                ('line4', 4),
                ('line5', 5),
                ('line6', 6),
                ('line7', 7),
                ('line8', 8),
                ('line9', 9),
            ],
        )

    def test_get_lines_reverse(self):
        self.gotoLine(9)
        self.assertEqual(
            list(self.context.lines(to_line=1)),
            [
                ('line9', 9),
                ('line8', 8),
                ('line7', 7),
                ('line6', 6),
                ('line5', 5),
                ('line4', 4),
                ('line3', 3),
                ('line2', 2),
                ('line1', 1),
            ],
        )

    def test_get_lines_range(self):
        self.assertEqual(
            list(self.context.lines(from_line=2, to_line=5)),
            [
                ('line2', 2),
                ('line3', 3),
                ('line4', 4),
                ('line5', 5),
            ],
        )

    def test_get_lines_reverse_range(self):
        self.assertEqual(
            list(self.context.lines(from_line=5, to_line=2)),
            [
                ('line5', 5),
                ('line4', 4),
                ('line3', 3),
                ('line2', 2),
            ],
        )

    def test_get_lines_one_line(self):
        self.assertEqual(
            list(self.context.lines(from_line=4, to_line=4)), [('line4', 4)]
        )
