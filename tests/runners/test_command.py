from AnyTest.plugin.runners.command import Runner as CommandRunner
from AnyTest.tests import SublimeWindowTestCase


class CommandRunnerTestCase(SublimeWindowTestCase):
    def test_get_panel_name(self):
        runner = CommandRunner(
            'scope', 'cmd', 'dir', 'file', 'line', 'language', 'framework', {}
        )

        self.assertEqual(runner.get_panel_name(), CommandRunner.panel_name)

    def test_get_panel_name_from_options(self):
        runner = CommandRunner(
            'scope',
            'cmd',
            'dir',
            'file',
            'line',
            'language',
            'framework',
            {'panel_name': 'my_panel_name'},
        )

        self.assertEqual(runner.get_panel_name(), 'my_panel_name')
        self.assertEqual(runner.options, {})

    def test_get_command_name(self):
        runner = CommandRunner(
            'scope',
            'cmd',
            'dir',
            'file',
            'line',
            'language',
            'framework',
            {},
        )

        self.assertEqual(runner.get_command_name(), CommandRunner.DEFAULT_COMMAND_NAME)
        self.assertEqual(runner.options, {})

    def test_get_command_name_from_options(self):
        runner = CommandRunner(
            'scope',
            'cmd',
            'dir',
            'file',
            'line',
            'language',
            'framework',
            {'command_name': 'my_command_name'},
        )

        self.assertEqual(runner.get_command_name(), 'my_command_name')
        self.assertEqual(runner.options, {})
