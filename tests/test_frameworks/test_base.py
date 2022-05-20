from AnyTest.plugin.test_frameworks import TestFramework, items, load, quick_panel_items
from AnyTest.tests import SublimeWindowTestCase


class TF(TestFramework):
    language = '_lng'
    framework = '_frm'


class BaseTestFrameworkTestCase(SublimeWindowTestCase):
    def test_settings_read_from_framework_settings(self):
        self.setSettings({'_lng._frm.key': 'value'})

        self.assertEqual(TF.settings('key'), 'value')

    def test_settings_default_value(self):
        self.assertEqual(TF.settings('key', default='value'), 'value')

    def test_settings_type(self):
        self.setSettings({'_lng._frm.key': 'value'})

        self.assertIsNone(TF.settings('key', type=bool))

    def test_settings_language_level_settings(self):
        self.setSettings({'_lng._frm.key': 'value1', '_lng.key': 'value2'})

        self.assertEqual(TF.settings('key', framework=False), 'value2')

    def test_settings_fallback_from_framework_to_language(self):
        self.setSettings({'_lng.key': 'value'})

        self.assertEqual(TF.settings('key', fallback=True), 'value')

    def test_settings_fallback_from_language_to_root(self):
        self.setSettings({'_lng._frm.key': 'value1', 'key': 'value2'})

        self.assertEqual(
            TF.settings('key', framework=False, fallback=True, root=True), 'value2'
        )

    def test_settings_fallback_from_framework_to_root(self):
        self.setSettings({'key': 'value'})

        self.assertEqual(TF.settings('key', fallback=True, root=True), 'value')

    def test_settings_merge_framework_with_language(self):
        self.setSettings({'_lng._frm._ENV': {'B': 1}, '_lng._ENV': {'A': 1}})

        self.assertEqual(TF.settings('_ENV', merge=True), {'A': 1, 'B': 1})

    def test_settings_merge_language_with_root(self):
        self.setSettings({'_lng._ENV': {'C': 1}, '_ENV': {'D': 1}})

        self.assertEqual(
            TF.settings('_ENV', framework=False, root=True, merge=True),
            {'C': 1, 'D': 1},
        )

    def test_settings_merge_framework_with_language_with_root(self):
        self.setSettings(
            {'_lng._frm._ENV': {'E': 1}, '_lng._ENV': {'F': 1}, '_ENV': {'G': 1}}
        )

        self.assertEqual(
            TF.settings('_ENV', root=True, merge=True), {'E': 1, 'F': 1, 'G': 1}
        )


class FunctionsTestCase(SublimeWindowTestCase):
    def test_load(self):
        test_framework = load('ruby', 'rspec')

        self.assertTrue(issubclass(test_framework, TestFramework))
        self.assertEqual(test_framework.language, 'ruby')
        self.assertEqual(test_framework.framework, 'rspec')

    def test_load_not_found(self):
        with self.assertRaises(ImportError):
            load('_lng', '_frm')

    def test_items(self):
        self.setSettings(
            {'test_frameworks': {'ruby': 'rspec', 'python': ['pyunit'], '_lng': '_frm'}}
        )
        test_frameworks = list(items())

        self.assertEqual(len(test_frameworks), 2)
        self.assertTrue(
            any(
                item
                for item in test_frameworks
                if item.language == 'ruby' and item.framework == 'rspec'
            )
        )
        self.assertTrue(
            any(
                item
                for item in test_frameworks
                if item.language == 'python' and item.framework == 'pyunit'
            )
        )
