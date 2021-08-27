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
                return cls(folder)
        else:
            raise errors.InvalidContext(
                "File '{}' is outside of the project".format(file)
            )

    def join(self, *paths):
        return os.path.join(self.path, *paths)

    def file_exist(self, *paths):
        return os.path.isfile(self.join(*paths))

    def relpath(self, file):
        return os.path.relpath(file, self.path)
