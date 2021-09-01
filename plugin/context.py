import re
from collections import namedtuple
from functools import lru_cache

from .root import Root
from .mixins import WindowMixin


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
    def __init__(self, view):
        self.view = view
        self.root, self.file = Root.find(self.window().folders(), self.view.file_name())

    def window(self):
        return self.view.window()

    def get_line(self, point):
        line, _ = self.view.rowcol(point)

        return int(line) + 1

    @lru_cache(maxsize=None)
    def sel_lines(self):
        return [self.get_line(r.begin()) for r in self.view.sel()]

    @lru_cache(maxsize=None)
    def sel_line(self):
        return next(iter(self.sel_lines()), 1)

    def lines(self, forward=False):
        point = self.view.sel()[0].begin()
        line_nr = self.get_line(point)
        view_size = self.view.size()

        while 0 <= point <= view_size:
            line_region = self.view.line(point)
            line = self.view.substr(line_region)

            yield line, line_nr

            if forward:
                point = line_region.end() + 1
                line_nr += 1
            else:
                point = line_region.begin() - 1
                line_nr -= 1

    def find_nearest(self, test_patterns, namespace_patterns=(), forward=False):
        tests = []
        namespaces = []
        names = []
        test_line_nr = None
        last_namespace_line_nr = last_indent = -1

        for line, line_nr in self.lines(forward=forward):
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

        return Nearest(tests, namespaces, test_line_nr, names)
