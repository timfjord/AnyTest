import os.path

from ... import utils
from ...errors import Error
from .. import python
from ..mixins import IsConfigurableMixin


class TestFramework(IsConfigurableMixin, python.TestFramework):
    MAX_DEPTH = 20
    NEAREST_SEPARATOR = "."
    SEPARATOR_NOSE = ":"

    framework = "django"  # type: str
    pattern = r"test.*\.py$"  # type: str

    @classmethod
    def is_configurable_fallback(cls, file):
        return file.root.file("manage.py").exists() and utils.is_executable(
            "django-admin"
        )

    def build_executable(self):
        return self._build_executable(["python", "manage.py", "test"])

    def get_import_path(self):
        folder = self.context.file.dir()

        for _ in range(self.MAX_DEPTH):
            if folder.file("__init__.py").exists():
                relpath = folder.parent().relpath(self.context.file.path)
                path, _ = os.path.splitext(relpath)

                return self.path_to_module(path)

            folder = folder.parent()

        raise Error("Couldn't find import path")

    def build_file_position_args(self):
        return [self.get_import_path()]

    def build_line_position_args(self):
        name = self.find_nearest().join(self.NEAREST_SEPARATOR)

        if bool(name):
            separator = (
                self.SEPARATOR_NOSE
                if self.settings("use_nose", type=bool)
                else self.NEAREST_SEPARATOR
            )
            return [separator.join([self.get_import_path(), name])]
        else:
            return self.build_file_position_args()
