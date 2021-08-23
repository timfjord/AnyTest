import os.path
from functools import lru_cache

from . import errors


class Views:
    def __init__(self, view):
        self.view = view
        self.fallback = False

    @lru_cache(maxsize=None)
    def fallback_views(self):
        return iter(self.view.window().views())

    def __iter__(self):
        self.fallback = False

        return self

    def __next__(self):
        if self.fallback:
            return next(self.fallback_views())
        else:
            self.fallback = True
            return self.view


class Context:
    def __init__(self, view):
        self.view = view

    @classmethod
    def find(cls, view):
        if not bool(view.window().folders()):
            raise errors.InvalidContext

        for view in Views(view):
            if bool(view.file_name()):
                return cls(view)
        else:
            raise errors.InvalidContext

    @lru_cache(maxsize=None)
    def root(self):
        return self.view.window().folders()[0]

    def file_exists(self, *paths):
        return os.path.isfile(os.path.join(self.root(), *paths))

    @lru_cache(maxsize=None)
    def file(self):
        return os.path.relpath(self.view.file_name(), self.root())

    def get_line(self, region):
        line, _ = self.view.rowcol(region.begin())

        return int(line) + 1

    @lru_cache(maxsize=None)
    def lines(self):
        return [self.get_line(region) for region in self.view.sel()]

    @lru_cache(maxsize=None)
    def line(self):
        return next(iter(self.lines()), 1)

    def save(self):
        self.view.window().run_command('save')

    def save_all(self):
        self.view.window().run_command('save_all')

    def find_nearest(self):
        pass
