from ..runners import Command
from ..runners import Runner as BaseRunner
from ..test_frameworks import TestFramework


class Runner(BaseRunner):
    name = 'unittesting'
    panel_name = 'output.UnitTesting'

    def __init__(self, test_framework, scope):
        self.test_framework = test_framework
        self.command = Command(
            scope,
            # we care only about the last part when it comes to unittesting
            # as this is where the module part of the pyunit test framework command
            # can be found
            test_framework.build_command(scope)[-1],
            test_framework.context.root.path,
            test_framework.context.file.path,
            test_framework.context.sel_line(),
            test_framework.language,
            test_framework.framework,
        )

    def run(self):
        if self.command.scope == TestFramework.SCOPE_SUITE:
            self.run_command('unit_testing_current_package')
        else:
            self.run_command('unit_testing_current_file')
