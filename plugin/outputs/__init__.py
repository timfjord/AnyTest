import importlib
from abc import ABCMeta, abstractmethod

from .. import settings, test_frameworks


def load(output):
    module = importlib.import_module('.{}'.format(output), __name__)
    return getattr(module, 'Output')


def build(command, test_framework=None):
    if test_framework is None:
        test_framework = test_frameworks.load(command.language, command.framework)

    output_name = test_framework.settings(
        'output', type=str, default='console', root=True
    )
    output = load(output_name)

    output(command, test_framework).build()


class Output(metaclass=ABCMeta):
    name = None

    def __init__(self, command, test_framework):
        self.command = command
        self.test_framework = test_framework

    def settings(self, key, default=None, type=None):
        if self.name is None:
            raise NotImplementedError('name is not defined for the output')

        return settings.get(('output', self.name, key), type=type, default=default)

    @abstractmethod
    def build(self):
        pass
