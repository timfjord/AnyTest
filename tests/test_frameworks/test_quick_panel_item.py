# isort:skip_file
import unittest

import sublime

from AnyTest.plugin.test_frameworks.quick_panel_item import QuickPanelItem


class QuickPanelItemTestCase(unittest.TestCase):
    def setUp(self):
        self.item = QuickPanelItem('language', 'framework')

    def test_base(self):
        base_class = list if sublime.version() < '4000' else sublime.QuickPanelItem

        self.assertIsInstance(self.item, base_class)

    def test_properties(self):
        self.assertEqual(self.item.language, 'language')
        self.assertEqual(self.item.framework, 'framework')

    def test_signature(self):
        self.assertEqual(self.item.signature(), ('language', 'framework'))
