from ..runners import Runner as BaseRunner


SETTINS_KEY = 'last_command'


class Runner(BaseRunner):
    name = 'test'

    def run(self):
        print('--- AnyTest command ---')
        print(self.command)
        print('-----------------------')

        self.test_framework.context.view.settings().set(SETTINS_KEY, self.command.cmd)
