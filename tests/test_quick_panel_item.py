# isort:skip_file
import unittest

import sublime

from AnyTest.tests import ST3
from AnyTest.plugin.quick_panel_item import QuickPanelItem


class QuickPanelItemTestCase(unittest.TestCase):
    def setUp(self):
        self.item = QuickPanelItem("trigger", "details", "annotation")

    def test_base(self):
        base_class = list if ST3 else sublime.QuickPanelItem

        self.assertIsInstance(self.item, base_class)

    @unittest.skipUnless(ST3, "Sublime Text 3 test")
    def test_base_st3(self):
        item = QuickPanelItem("trigger", "", "annotation")

        self.assertEqual(item, ["trigger", "annotation"])

    def test_properties(self):
        self.assertEqual(self.item.trigger, "trigger")
        self.assertEqual(self.item.details, "details")
        self.assertEqual(self.item.annotation, "annotation")
