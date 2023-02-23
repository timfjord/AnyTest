import os.path
import re
from functools import reduce

from ... import utils
from ...cache import cache
from .. import java
from ..mixins import IsConfigurableMixin

MAX_DEPTH = 20
POM_XML = 'pom.xml'


@cache
def get_pom_file(file):
    folder = file.parent()

    for _ in range(MAX_DEPTH):
        pom_file = folder.file(POM_XML)

        if pom_file.exists():
            return pom_file

        folder = folder.parent()


class TestFramework(IsConfigurableMixin, java.TestFramework):
    framework = 'maventest'
    pattern = r'([Tt]est.*|.*[Tt]est(s|Case)?)\.java$'

    @classmethod
    def is_configurable_fallback(cls, file):
        return bool(get_pom_file(file))

    def get_package(self):
        patterns = (
            (r'\\', '/'),
            (r'^.*src\/(main|test)\/(java\/)?', ''),
            (r'\/[^\/]+$', ''),
            (r'/', '.'),
        )

        return reduce(
            lambda value, args: re.sub(args[0], args[1], value),
            patterns,
            self.context.file.relpath,
        )

    def build_executable(self):
        mvnw = self.file('mvnw')

        if mvnw.exists():
            return ['./{}'.format(mvnw.relpath)]

        return ['mvn']

    def build_suite_position_args(self):
        args = ['test']
        pom_file = get_pom_file(self.context.file)

        if pom_file and pom_file.parent().file(POM_XML).exists():
            args += ['-pl', pom_file.dirname()]

        return args

    def build_file_position_args(self):
        args = self.build_suite_position_args()

        return args + [
            '-Dtest=' + self.get_package() + '.' + self.context.file.name() + r'\*'
        ]

    def build_line_position_args(self):
        nearest = self.find_nearest()
        name = ''.join(
            (
                utils.escape_regex('$'.join(nearest.namespaces)),
                '#' if bool(nearest.namespaces) else '',
                utils.escape_regex('$'.join(nearest.tests)),
            )
        )

        if bool(name):
            args = self.build_suite_position_args()

            return args + ['-Dtest=' + self.get_package() + '.' + name]
        else:
            return self.build_file_position_args()
