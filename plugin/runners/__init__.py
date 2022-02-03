import importlib
import re
from abc import ABCMeta, abstractmethod
from collections import OrderedDict, namedtuple

from .. import errors, settings
from ..mixins import WindowMixin


def load(runner):
    module = importlib.import_module('.{}'.format(runner), __name__)
    return getattr(module, 'Runner')


def find(test_framework):
    runner_name = test_framework.settings(
        'runner', type=str, default='command', root=True
    )
    return load(runner_name)


class Runner(
    WindowMixin,
    namedtuple('Runner', 'scope, cmd, dir, file, line, language, framework, options'),
    metaclass=ABCMeta,
):
    __slots__ = ()

    name = None
    panel_name = None

    @classmethod
    def build(cls, test_framework, scope):
        return cls(*cls.Builder(test_framework, scope).build())

    @classmethod
    def settings(cls, key, default=None, type=None):
        if cls.name is None:
            raise NotImplementedError('name is not defined for the runner')

        return settings.get(('runner', cls.name, key), type=type, default=default)

    def get_panel_name(self):
        if self.panel_name is None:
            raise errors.Error('panel_name is not set')

        return self.panel_name

    def show_output(self, focus=True):
        panel_name = self.get_panel_name()

        self.window.run_command('show_panel', args={'panel': panel_name})

        if not focus:
            return

        panel = self.window.find_output_panel(re.sub(r'^output\.', '', panel_name))

        if panel:
            self.window.focus_view(panel)

    def to_dict(self):
        # cannot use _asdict, see https://stackoverflow.com/a/40677996/1078179
        return OrderedDict(zip(self._fields, self))

    @abstractmethod
    def run(self):
        pass

    class Builder:
        def __init__(self, test_framework, scope):
            self.test_framework = test_framework
            self.scope = scope

        def build_cmd(self):
            return ' '.join(self.test_framework.build_command(self.scope))

        def build_dir(self):
            return self.test_framework.context.root.path

        def build_file(self):
            return self.test_framework.context.file.path

        def build_line(self):
            return self.test_framework.context.sel_line()

        def build_language(self):
            return self.test_framework.language

        def build_framework(self):
            return self.test_framework.framework

        def build_options(self):
            return {}

        def build(self):
            return (
                self.scope,
                self.build_cmd(),
                self.build_dir(),
                self.build_file(),
                self.build_line(),
                self.build_language(),
                self.build_framework(),
                self.build_options(),
            )
