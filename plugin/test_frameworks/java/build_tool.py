import re
from abc import ABCMeta, abstractmethod
from functools import reduce

from ... import utils
from ...cache import cache
from ...errors import Error


def find(file):
    for build_tool_type in (Maven, Gradle):
        build_tool = build_tool_type(file)

        if bool(build_tool.config_file):
            return build_tool

    raise Error("Couldn't find a build tool")


class Base(metaclass=ABCMeta):
    MAX_DEPTH = 20
    NAMESPACE_SEPARATOR = '$'

    @property
    @abstractmethod
    def executable(self):
        pass

    @property
    @abstractmethod
    def config_filenames(self):
        pass

    @classmethod
    def find_config_file(cls, folder, max_depth=MAX_DEPTH):
        for _ in range(max_depth):
            for filename in cls.config_filenames:
                config_file = folder.file(filename)

                if config_file.exists():
                    return config_file

            folder = folder.parent()

    def __init__(self, file):
        self.file = file

    @property
    @cache
    def config_file(self):
        return self.find_config_file(self.file.dir())

    @abstractmethod
    def build_module_args(self, module):
        pass

    @abstractmethod
    def build_file_position_args(self):
        pass

    @abstractmethod
    def build_line_position_args(self, _):
        pass


class Maven(Base):
    PACKAGE_REPLACEMENTS = (
        (r'\\', '/'),
        (r'^.*src\/(main|test)\/(java\/)?', ''),
        (r'\/[^\/]+$', ''),
        (r'/', '.'),
    )
    NEAREST_SEPARATOR = '$'
    SECTION_SEPARATOR = '#'

    executable = 'mvn'  # type: str
    config_filenames = ('pom.xml',)  # type: tuple

    def get_package(self):
        return reduce(
            lambda value, args: re.sub(args[0], args[1], value),
            self.PACKAGE_REPLACEMENTS,
            self.file.relpath,
        )

    def build_module_args(self, module):
        return ['-pl', module]

    def build_file_position_args(self):
        return ['-Dtest=' + self.get_package() + '.' + self.file.name() + r'\*']

    def build_line_position_args(self, nearest):
        name = ''.join(
            (
                utils.escape_regex(self.NAMESPACE_SEPARATOR.join(nearest.namespaces)),
                self.SECTION_SEPARATOR if bool(nearest.namespaces) else '',
                utils.escape_regex(self.NEAREST_SEPARATOR.join(nearest.tests)),
            )
        )

        if bool(name):
            return ['-Dtest=' + self.get_package() + '.' + name]


class Gradle(Base):
    NEAREST_SEPARATOR = '.'

    executable = 'gradle'  # type: str
    config_filenames = (
        'build.gradle',
        'build.gradle.kts',
        'settings.gradle',
        'settings.gradle.kts',
    )  # type: tuple

    def build_module_args(self, module):
        return ['-p', module]

    def build_file_position_args(self):
        return ['--tests', self.file.name()]

    def build_line_position_args(self, nearest):
        name = ''.join(
            (
                utils.escape_regex(self.NAMESPACE_SEPARATOR.join(nearest.namespaces)),
                self.NEAREST_SEPARATOR if bool(nearest.namespaces) else '',
                utils.escape_regex(self.NEAREST_SEPARATOR.join(nearest.tests)),
            )
        )

        if bool(name):
            return ['--tests', name]
