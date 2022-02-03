from AnyTest.plugin.runners import Runner as BaseRunner
from AnyTest.tests import SublimeWindowTestCase


class Runner(BaseRunner):
    name = '_rnr'

    def run(self):
        pass


class BaseRunnerTestCase(SublimeWindowTestCase):
    def test_init(self):
        runner = Runner(
            'scope', 'cmd', 'dir', 'file', 'line', 'language', 'framework', {}
        )

        self.assertEqual(runner.scope, 'scope')
        self.assertEqual(runner.cmd, 'cmd')
        self.assertEqual(runner.dir, 'dir')
        self.assertEqual(runner.file, 'file')
        self.assertEqual(runner.line, 'line')
        self.assertEqual(runner.language, 'language')
        self.assertEqual(runner.framework, 'framework')
        self.assertEqual(runner.options, {})

        self.assertEqual(
            runner.to_dict(),
            {
                'scope': 'scope',
                'cmd': 'cmd',
                'dir': 'dir',
                'file': 'file',
                'line': 'line',
                'language': 'language',
                'framework': 'framework',
                'options': {},
            },
        )

    def test_settings(self):
        self.assertIsNone(Runner.settings('something'))

        self.setSettings({'runner._rnr.something': 'value'})

        self.assertEqual(Runner.settings('something'), 'value')

    def test_settings_raise_error_when_no_name(self):
        with self.assertRaises(NotImplementedError):
            BaseRunner.settings('something')
