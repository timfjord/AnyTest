from unittest import mock

from AnyTest.plugin.quick_panel_item import QuickPanelItem
from AnyTest.tests import SublimeProjectTestCase


class HistroryTestCase(SublimeProjectTestCase):
    folder = 'rspec'

    def test_show_clear_history(self):
        project_dir = self.window.folders()[0]

        yield from self._testFile('normal_spec.rb', 1)
        yield from self._testSuite('normal_spec.rb')
        yield from self._testFile('normal_spec.rb')

        with mock.patch('sublime.Window.show_quick_panel') as show_quick_panel_mock:
            self.view.run_command('any_test_show_history')

            self.assertTrue(show_quick_panel_mock.called)

            items = show_quick_panel_mock.call_args[0][0]

            self.assertIsInstance(items[0], QuickPanelItem)
            self.assertEqual(items[0].trigger, 'normal_spec.rb')
            self.assertEqual(
                items[0].details, "[file] in '{}' with console".format(project_dir)
            ),
            self.assertEqual(items[0].annotation, 'rspec')

            self.assertIsInstance(items[1], QuickPanelItem)
            self.assertEqual(items[1].trigger, 'rspec')
            self.assertEqual(
                items[1].details, "[suite] in '{}' with console".format(project_dir)
            ),
            self.assertEqual(items[1].annotation, 'rspec')

            self.assertIsInstance(items[2], QuickPanelItem)
            self.assertEqual(items[2].trigger, 'normal_spec.rb:1')
            self.assertEqual(
                items[2].details, "[line] in '{}' with console".format(project_dir)
            ),
            self.assertEqual(items[2].annotation, 'rspec')

            show_quick_panel_mock.reset_mock()
            self.window.run_command('any_test_clear_history')
            self.window.run_command('any_test_show_history')

            self.assertFalse(show_quick_panel_mock.called)
