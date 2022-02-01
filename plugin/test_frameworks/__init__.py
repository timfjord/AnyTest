from abc import ABCMeta, abstractmethod
import importlib
import re

from .. import errors, logger, settings
from . import utils


# fmt: off
ALL = {
    'elixir': ['espec', 'exunit'],
    'javascript': ['jest'],
    'python': ['pytest', 'pyunit'],
    'ruby': ['minitest', 'rspec'],
}
# fmt: on


def load(language, framework):
    module = importlib.import_module(
        '..test_frameworks.{}.{}'.format(language.lower(), framework.lower()), __name__
    )
    return getattr(module, 'TestFramework')


def items():
    test_frameworks = settings.get('test_frameworks', type=dict)
    if not bool(test_frameworks):
        test_frameworks = ALL

    for language, frameworks in test_frameworks.items():
        for framework in utils.to_unpackable(frameworks):
            try:
                yield load(language, framework)
            except ImportError:
                logger.log(
                    "Cannot load '{}' framework for '{}' language".format(
                        framework, language
                    )
                )
                continue


def find(file):
    for framework in items():
        if framework.is_suitable_for(file):
            return framework

    raise errors.FrameworkNotFound


def _safe_merge(dict1, dict2):
    if not isinstance(dict1, dict):
        dict1 = {}

    if not isinstance(dict2, dict):
        dict2 = {}

    return dict(dict1, **dict2)


class TestFramework(metaclass=ABCMeta):
    SCOPE_SUITE = 'suite'
    SCOPE_FILE = 'file'
    SCOPE_LINE = 'line'

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
        cls,
        key,
        type=None,
        default=None,
        framework=True,
        root=False,
        fallback=True,
        merge=False,
    ):
        prefix = (cls.language,)

        if framework:
            prefix += (cls.framework,)

        value = settings.get(prefix + (key,), type=type)

        if fallback and value is None or merge:
            for i in range(1, -1 if root else 0, -1):
                prev_value = settings.get(prefix[:i] + (key,), type=type)

                if merge and (isinstance(value, dict) or isinstance(prev_value, dict)):
                    value = _safe_merge(prev_value, value)
                elif fallback and prev_value is not None:
                    value = prev_value
                    break

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
            self.settings('executable', type=list, fallback=False)
            or self.build_executable()
        )

    @abstractmethod
    def build_executable(self):
        pass

    def args(self):
        return self.settings('args', type=list, fallback=False, default=[])

    def build_suite_position_args(self):
        return []

    @abstractmethod
    def build_file_position_args(self):
        pass

    @abstractmethod
    def build_line_position_args(self):
        pass

    def build_command(self, scope):
        try:
            position_args = getattr(self, 'build_{}_position_args'.format(scope))

            return self.executable() + self.args() + position_args()
        except AttributeError:
            raise errors.Error('Invalid scope')
