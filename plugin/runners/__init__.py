import importlib
import re
from abc import ABCMeta, abstractmethod
from collections import namedtuple

from .. import settings
from ..mixins import WindowMixin


def load(runner):
    module = importlib.import_module('.{}'.format(runner), __name__)
    return getattr(module, 'Runner')


def find(test_framework):
    runner_name = test_framework.settings(
        'runner', type=str, default='command', root=True
    )
    return load(runner_name)


Command = namedtuple('Command', 'scope, cmd, dir, file, line, language, framework')


class Runner(WindowMixin, metaclass=ABCMeta):
    __slots__ = ()

    name = None
    panel_name = None

    def __init__(self, test_framework, scope):
        self.test_framework = test_framework
        self.command = Command(
            scope,
            ' '.join(test_framework.build_command(scope)),
            test_framework.context.root.path,
            test_framework.context.file.path,
            test_framework.context.sel_line(),
            test_framework.language,
            test_framework.framework,
        )

    def settings(self, key, default=None, type=None):
        if self.name is None:
            raise NotImplementedError('name is not defined for the runner')

        return settings.get(('runner', self.name, key), type=type, default=default)

    def toogle_output_focus(self):
        if self.panel_name is None:
            raise ValueError('panel_name is not set')

        view_to_focus = None

        if self.window.active_panel() == self.panel_name:
            view_to_focus = self.window.active_view()
        else:
            self.window.run_command('show_panel', args={'panel': self.panel_name})
            view_to_focus = self.window.find_output_panel(
                re.sub(r'^output\.', '', self.panel_name)
            )

        if view_to_focus:
            self.window.focus_view(view_to_focus)

    @abstractmethod
    def run(self):
        pass
