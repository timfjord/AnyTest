from ..runners import Runner as BaseRunner
from ..test_frameworks import TestFramework


class Runner(BaseRunner):
    name = 'unittesting'
    panel_name = 'output.UnitTesting'

    def run(self):
        if self.scope == TestFramework.SCOPE_SUITE:
            self.run_command('unit_testing_current_package')
        else:
            self.run_command('unit_testing_current_file')

    class Builder(BaseRunner.Builder):
        def build_cmd(self):
            # we care only about the last part when it comes to unittesting
            # as this is where the module part of the pyunit test framework command can be found
            return self.test_framework.build_command(self.scope)[-1]
