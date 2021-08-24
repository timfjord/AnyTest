from ..outputs import Output as BaseOutput


class Output(BaseOutput):
    name = 'console'

    def build(self):
        print('--- AnyTest command ---')
        print(self.command)
        print('-----------------------')
