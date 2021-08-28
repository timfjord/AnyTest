import os.path

from . import errors


class Root:
    def __init__(self, path):
        self.path = path

    @classmethod
    def find(cls, folders, file):
        if not bool(file):
            raise errors.InvalidContext

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

    def join(self, *paths):
        return os.path.join(self.path, *paths)

    def relpath(self, file):
        return os.path.relpath(file, self.path)

    def file(self, *paths):
        return File(self, *paths)


class File:
    def __init__(self, root, *paths):
        if not bool(paths):
            raise ValueError('Path is required')

        self.root = root
        self.relpath = os.path.join(*paths)
        self.path = self.root.join(self.relpath)

    def exists(self):
        return os.path.exists(self.path)
