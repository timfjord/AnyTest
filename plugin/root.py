import os.path

from . import errors, glob2
from .utils import to_unpackable


class Root:
    def __init__(self, path):
        self.path = path

    @classmethod
    def find(cls, folders, file, subprojects=[]):
        if not bool(file) or not bool(folders):
            raise errors.InvalidContext

        root = cls(folders[0])
        for subproject in subprojects:
            folders.append(
                root.join(*to_unpackable(subproject)),
            )

        for folder in sorted(folders, key=len, reverse=True):
            # Since Sublime returns expanded path so it should be fine to use `startswith`,
            # but more future-proof solution would be using `pathlib.Path`
            if file.startswith(folder):
                root = cls(folder)
                relpath = root.relpath(file)

                return (root, root.file(relpath))
        else:
            raise errors.InvalidContext(
                "File '{}' is outside of the project".format(file)
            )

    def name(self):
        return os.path.basename(self.path)

    def join(self, *paths):
        return os.path.join(self.path, *paths)

    def relpath(self, file):
        return os.path.relpath(file, self.path)

    def file(self, *paths):
        return File(self, *paths)

    def parent(self):
        return Root(os.path.dirname(self.path))

    def glob(self, *paths):
        return Glob(self, *paths)


class RelativePath:
    def __init__(self, root, *paths):
        if not bool(paths):
            raise ValueError('Path is required')

        self.root = root
        self.relpath = os.path.join(*paths)
        self.path = self.root.join(self.relpath)

    def exists(self):
        return os.path.exists(self.path)

    def contains(self, _):
        raise NotImplementedError()

    def dir(self):
        return Root(os.path.dirname(self.path))

    def dirname(self):
        return self.dir().name()

    def parent(self):
        return self.dir().parent()

    def name(self):
        return os.path.splitext(
            os.path.basename(self.relpath),
        )[0]


class File(RelativePath):
    def exists(self):
        return os.path.isfile(self.path)

    def contains(self, content):
        with open(self.path) as file:
            return content in file.read()


class Glob:
    def __init__(self, root, *paths):
        if not bool(paths):
            raise ValueError('Path is required')

        self.root = root
        self.pattern = self.root.join(*paths)

    def __iter__(self):
        return glob2.iglob(self.pattern)
