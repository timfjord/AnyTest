from functools import lru_cache

from .root import Root
from .window import Window


class Context(Window):
    def __init__(self, view):
        self.view = view
        self.root, self.file = Root.find(self.window().folders(), self.view.file_name())

    def window(self):
        return self.view.window()

    def get_line(self, region):
        line, _ = self.view.rowcol(region.begin())

        return int(line) + 1

    @lru_cache(maxsize=None)
    def sel_lines(self):
        return [self.get_line(region) for region in self.view.sel()]

    @lru_cache(maxsize=None)
    def sel_line(self):
        return next(iter(self.sel_lines()), 1)

    def find_nearest(self):
        pass
