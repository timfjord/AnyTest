import importlib
from abc import ABCMeta, abstractmethod

from .. import settings, test_frameworks


def build(command, test_framework=None):
    if test_framework is None:
        test_framework = test_frameworks.load(command.language, command.framework)

    output = test_framework.settings('output', type=str, default='panel')

    module = importlib.import_module(".{}".format(output), __name__)
    output = getattr(module, 'Output')

    output(command, test_framework).build()


class Output(metaclass=ABCMeta):
    settings_key = None

    def __init__(self, command, test_framework):
        self.command = command
        self.test_framework = test_framework

    def settings(self, key, default=None, type=None):
        if self.settings_key is None:
            raise NotImplementedError('settings_key is not defined for the output')

        return settings.get(
            ('output', self.settings_key, key), type=type, default=default
        )

    @abstractmethod
    def build(self):
        pass
