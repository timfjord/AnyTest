import os.path

from . import errors


class Root:
    def __init__(self, path):
        self.path = path

    @classmethod
    def find(cls, folders, file):
        if not bool(folders):
            raise errors.InvalidContext("Couldn't find project")

        if not bool(file):
            raise errors.InvalidContext

        for folder in sorted(folders, key=len, reverse=True):
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
