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
    """
    Prints the command in the console and saves the cmd value in the current view.
    Useful when there is no need to actually run the command(e.g. in tests, for debugging)
    """

    name = 'console'
    panel_name = 'console'

    def run(self):
        print('--- AnyTest command ---')
        print(self.command)
        print('-----------------------')

        last_command(self.test_framework.context.view, self.command.cmd)
