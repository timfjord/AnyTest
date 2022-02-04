import os.path

from ..runners import Runner as BaseRunner
from ..test_frameworks import TestFramework


class Runner(BaseRunner):
    name = 'unittesting'
    panel_name = 'output.UnitTesting'

    def run(self):
        args = {'package': os.path.basename(self.dir)}

        if self.scope != TestFramework.SCOPE_SUITE:
            args['pattern'] = os.path.basename(self.file)
            args['package'] += ':{}'.format(args['pattern'])

        self.run_command('unit_testing', args=args)

    class Builder(BaseRunner.Builder):
        def build_cmd(self):
            # we care only about the last part when it comes to unittesting
            # as this is where the module part of the pyunit test framework command can be found
            return self.test_framework.build_command(self.scope)[-1]
