import re
from collections import namedtuple
from functools import lru_cache
from operator import ge, le

from .mixins import WindowMixin
from .root import Root

Nearest = namedtuple('Nearest', 'tests, namespaces, line, names')


def _match_patterns(string, patterns):
    for pattern in patterns:
        if isinstance(pattern, tuple):
            pattern, name = pattern
        else:
            name = None

        match = re.search(pattern, string)
        if match is not None:
            return match.group(1), name

    return None, None


class Context(WindowMixin):
    CURRENT_LINE = 'current'

    def __init__(self, view):
        self.view = view
        self.root, self.file = Root.find(self.window.folders(), self.view.file_name())

    @property
    def window(self):
        return self.view.window()

    def get_line(self, point):
        line, _ = self.view.rowcol(point)

        return int(line) + 1

    def get_current_line(self):
        point = self.view.sel()[0].begin()

        return self.get_line(point), point

    @lru_cache(maxsize=None)
    def sel_lines(self):
        return [self.get_line(r.begin()) for r in self.view.sel()]

    @lru_cache(maxsize=None)
    def sel_line(self):
        return next(iter(self.sel_lines()), 1)

    def lines(self, from_line=None, to_line=None):
        if from_line is None:
            line_nr, point = self.get_current_line()
        else:
            line_nr = from_line
            point = self.view.text_point(from_line - 1, 0)

        if to_line is None:
            to_line = self.get_line(self.view.size())
        elif to_line == self.CURRENT_LINE:
            to_line, _ = self.get_current_line()

        forward = line_nr < to_line
        operator = le if forward else ge

        while operator(line_nr, to_line):
            line_region = self.view.line(point)
            line = self.view.substr(line_region)

            yield line, line_nr

            if forward:
                point = line_region.end() + 1
                line_nr += 1
            else:
                point = line_region.begin() - 1
                line_nr -= 1

    def find_nearest(
        self,
        test_patterns,
        namespace_patterns=(),
        from_line=None,
        to_line=None,
    ):
        tests = []
        namespaces = []
        names = []
        test_line_nr = None
        last_namespace_line_nr = last_indent = -1

        for line, line_nr in self.lines(from_line=from_line, to_line=to_line):
            test_match, test_name = _match_patterns(line, test_patterns)
            namespace_match, _ = _match_patterns(line, namespace_patterns)
            indent_match = re.match(r'^\s*', line)
            indent = 0 if indent_match is None else indent_match.end()

            if test_match and (
                last_indent == -1
                or (
                    test_line_nr is None
                    and last_indent > indent
                    and last_namespace_line_nr > line_nr
                    and last_namespace_line_nr != -1
                )
            ):
                if last_namespace_line_nr > line_nr:
                    namespaces = []
                    last_namespace_line_nr = -1
                tests.append(test_match)
                if test_name is not None:
                    names.append(test_name)
                last_indent = indent
                test_line_nr = line_nr
            elif namespace_match and (indent < last_indent or last_indent == -1):
                namespaces.append(namespace_match)
                last_indent = indent
                last_namespace_line_nr = line_nr

        return Nearest(tests, namespaces[::-1], test_line_nr, names)
