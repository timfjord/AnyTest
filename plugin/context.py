from functools import lru_cache

from .root import Root
from .window import Window


class Context(Window):
    def __init__(self, view):
        self.view = view
        self.root = Root.find(self.window().folders(), self.file())

    def window(self):
        return self.view.window()

    def directory(self):
        return self.root.path

    def file_exist(self, *paths):
        return self.root.file_exist(*paths)

    @lru_cache(maxsize=None)
    def file(self):
        return self.view.file_name()

    @lru_cache(maxsize=None)
    def file_relpath(self):
        return self.root.relpath(self.file())

    def get_line(self, region):
        line, _ = self.view.rowcol(region.begin())

        return int(line) + 1

    @lru_cache(maxsize=None)
    def lines(self):
        return [self.get_line(region) for region in self.view.sel()]

    @lru_cache(maxsize=None)
    def line(self):
        return next(iter(self.lines()), 1)

    def find_nearest(self):
        pass
