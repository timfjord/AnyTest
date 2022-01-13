import unittest

from AnyTest.plugin.test_frameworks import TestFramework
from AnyTest.tests import SublimeWindowTestCase


class TF(TestFramework):
    language = 'ruby'
    framework = 'rspec'


@unittest.skip
class TestFrameworkTestCase(SublimeWindowTestCase):
    def test_settings_read_from_framework_settings(self):
        self.setSettings({'ruby.rspec.key': 'value'})

        self.assertEqual(TF.settings('key'), 'value')

    def test_settings_default_value(self):
        self.assertEqual(TF.settings('key', default='value'), 'value')

    def test_settings_type(self):
        self.setSettings({'ruby.rspec.key': 'value'})

        self.assertIsNone(TF.settings('key', type=bool))

    def test_settings_language_level_settings(self):
        self.setSettings({'ruby.rspec.key': 'value1', 'ruby.key': 'value2'})

        self.assertEqual(TF.settings('key', framework=False), 'value2')

    def test_settings_fallback_from_framework_to_language(self):
        self.setSettings({'ruby.key': 'value'})

        self.assertEqual(TF.settings('key', fallback=True), 'value')

    def test_settings_fallback_from_language_to_root(self):
        self.setSettings({'ruby.rspec.key': 'value1', 'key': 'value2'})

        self.assertEqual(
            TF.settings('key', framework=False, fallback=True, root=True), 'value2'
        )

    def test_settings_fallback_from_framework_to_root(self):
        self.setSettings({'key': 'value'})

        self.assertEqual(TF.settings('key', fallback=True, root=True), 'value')

    def test_settings_merge_framework_with_language(self):
        self.setSettings({'ruby.rspec.ENV': {'B': 1}, 'ruby.ENV': {'A': 1}})

        self.assertEqual(TF.settings('ENV', merge=True), {'A': 1, 'B': 1})

    def test_settings_merge_language_with_root(self):
        self.setSettings({'ruby.ENV': {'C': 1}, 'ENV': {'D': 1}})

        self.assertEqual(
            TF.settings('ENV', framework=False, root=True, merge=True), {'C': 1, 'D': 1}
        )

    def test_settings_merge_framework_with_language_with_root(self):
        self.setSettings(
            {'ruby.rspec.ENV': {'E': 1}, 'ruby.ENV': {'F': 1}, 'ENV': {'G': 1}}
        )

        self.assertEqual(
            TF.settings('ENV', root=True, merge=True), {'E': 1, 'F': 1, 'G': 1}
        )
