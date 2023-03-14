from AnyTest.plugin.runners.command import Runner as CommandRunner
from AnyTest.tests import SublimeWindowTestCase


def build_runner(options={}):
    return CommandRunner(
        'scope', 'cmd', 'dir', 'file', 'line', 'language', 'framework', options, False
    )


class CommandRunnerTestCase(SublimeWindowTestCase):
    def test_get_panel_name(self):
        runner = build_runner()

        self.assertEqual(runner.get_panel_name(), CommandRunner.panel_name)

    def test_get_panel_name_from_options(self):
        runner = build_runner({'panel_name': 'my_panel_name'})

        self.assertEqual(runner.get_panel_name(), 'my_panel_name')
        self.assertEqual(runner.options, {})

    def test_get_command_name(self):
        runner = build_runner()

        self.assertEqual(runner.get_command_name(), CommandRunner.DEFAULT_COMMAND_NAME)
        self.assertEqual(runner.options, {})

    def test_get_command_name_from_options(self):
        runner = build_runner({'command_name': 'my_command_name'})

        self.assertEqual(runner.get_command_name(), 'my_command_name')
        self.assertEqual(runner.options, {})
