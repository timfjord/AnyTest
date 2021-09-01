import importlib
import re
from abc import ABCMeta, abstractmethod

from .. import settings


# fmt: off
ALL = {
    "JavaScript": ["Jest"],
    "Ruby": ["RSpec"]
}
# fmt: on


def load(language, framework):
    module = importlib.import_module(
        '..test_frameworks.{}.{}'.format(language.lower(), framework.lower()), __name__
    )
    return getattr(module, 'TestFramework')


def items():
    for language, frameworks in ALL.items():
        for framework in frameworks:
            yield load(language, framework)


def _safe_merge(dict1, dict2):
    if not isinstance(dict1, dict):
        dict1 = {}

    if not isinstance(dict2, dict):
        dict2 = {}

    return dict(dict1, **dict2)


class TestFramework(metaclass=ABCMeta):
    test_patterns = None
    namespace_patterns = []
    output_file_regex = None

    def __init__(self, context):
        self.context = context

    @property
    @abstractmethod
    def language(self):
        pass

    @property
    @abstractmethod
    def framework(self):
        pass

    @property
    @abstractmethod
    def pattern(self):
        pass

    @classmethod
    def is_suitable_for(cls, file):
        return re.search(cls.pattern, file.path)

    @classmethod
    def settings(
        cls, key, type=None, default=None, fallback=True, merge=False, language=False
    ):
        if language:
            return settings.get((cls.language, key), type=type, default=default)

        value = settings.get((cls.language, cls.framework, key), type=type)

        if fallback and value is None or merge:
            lang_value = settings.get((cls.language, key), type=type)

            if merge and (isinstance(value, dict) or isinstance(lang_value, dict)):
                value = _safe_merge(lang_value, value)
            elif fallback:
                value = lang_value

        return default if value is None else value

    def file(self, *path):
        return self.context.root.file(*path)

    def find_nearest(self, forward=False):
        if self.test_patterns is None:
            raise NotImplementedError('test_patterns is not defined for the framework')

        return self.context.find_nearest(
            self.test_patterns, self.namespace_patterns, forward=forward
        )

    def executable(self):
        return (
            self.settings('executable', fallback=False, type=list)
            or self.build_executable()
        )

    @abstractmethod
    def build_executable(self):
        pass

    def args(self):
        return self.settings('args', fallback=False, type=list) or self.build_args()

    def build_args(self):
        return []

    @abstractmethod
    def build_nearest_position_args(self):
        pass

    @abstractmethod
    def build_file_position_args(self):
        pass

    def build_suite_position_args(self):
        return []

    def build_command(self, scope):
        position_args = getattr(self, 'build_{}_position_args'.format(scope))

        return self.executable() + self.args() + position_args()
