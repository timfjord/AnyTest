from ..runners import Runner as BaseRunner


SETTINGS_KEY = 'any_test_last_command'


def last_command(view, value=None):
    if view is None:
        return ''

    settings = view.settings()

    if value is not None:
        settings.set(SETTINGS_KEY, value)

    return settings.get(SETTINGS_KEY)


class Runner(BaseRunner):
    name = 'test'

    def run(self):
        print('--- AnyTest command ---')
        print(self.command)
        print('-----------------------')

        last_command(self.test_framework.context.view, self.command.cmd)
