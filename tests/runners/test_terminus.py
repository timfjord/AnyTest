import unittest

from AnyTest.plugin.runners.terminus import Runner as TerminusRunner
from AnyTest.tests import SublimeWindowTestCase


class TerminusRunnerTestCase(SublimeWindowTestCase):
    def test_get_panel_name(self):
        runner = TerminusRunner(
            'scope',
            'cmd',
            'dir',
            'file',
            'line',
            'language',
            'framework',
            {'panel_name': 'my_panel_name'},
        )

        self.assertEqual(runner.get_panel_name(), TerminusRunner.panel_name)
        self.assertEqual(runner.options, {})

    def test_get_command_name(self):
        runner = TerminusRunner(
            'scope',
            'cmd',
            'dir',
            'file',
            'line',
            'language',
            'framework',
            {'command_name': 'my_command_name'},
        )

        self.assertEqual(runner.get_command_name(), TerminusRunner.COMMAND_NAME)
        self.assertEqual(runner.options, {})


class FakeTestFramework:
    def __init__(self, command):
        self.command = command

    def build_command(self, _):
        return [self.command]


class TerminusBuilderTestCase(unittest.TestCase):
    def assertBuiltCmd(self, command, expected):
        builder = TerminusRunner.Builder(FakeTestFramework(command), 'scope')
        self.assertEqual(builder.build_cmd(), expected)

    def test_build_cmd(self):
        self.assertBuiltCmd(
            r'go test -run TestNumbers/\\\[\\\]\\\.\\\*\\\+\\\?\\\|\\\$\\\^\\\(\\\)$ ./.',
            r'go test -run TestNumbers/\\\[\\\]\\\.\\\*\\\+\\\?\\\\\|\\\\\$\\\\\^\\\\\(\\\\\)\$ ./.',
        )
        self.assertBuiltCmd(
            r'do smth\$',
            r'do smth\$',
        )
