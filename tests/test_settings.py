import unittest

from AnyTest.plugin import settings
from AnyTest.tests import SublimeWindowTestCase


@unittest.skip
class SettingsTestCase(SublimeWindowTestCase):
    def test_unknown(self):
        self.assertIsNone(settings.get('unknown'))

    def test_settings(self):
        self.setSettings({'key.subkey': 'value'})

        self.assertEqual(settings.get('key.subkey'), 'value')

    def test_passing_an_iterator(self):
        self.setSettings({'key.subkey': 'value'})

        self.assertEqual(settings.get(('key', 'subkey')), 'value')

    def test_default(self):
        self.assertEqual(settings.get('unknown', default='value'), 'value')

    def test_typing(self):
        self.setSettings({'key': 'value'})

        self.assertEqual(settings.get('key', type=str), 'value')
        self.assertIsNone(settings.get('key', type=bool))


@unittest.skip
class ProjectSettingsTestCase(SublimeWindowTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.window.set_project_data(
            {'settings': {settings.PROJECT_SETTINGS_KEY: {'key': 'value2'}}}
        )

    def test_get(self):
        self.setSettings({'key': 'value1'})

        self.assertEqual(settings.get('key'), 'value2')


@unittest.skip
class InvalidProjectDataTestCase(SublimeWindowTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.window.set_project_data('invalid_data')

    def test_get(self):
        self.setSettings({'key': 'value'})

        self.assertEqual(settings.get('key'), 'value')


@unittest.skip
class InvalidProjectSettingsTestCase(SublimeWindowTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.window.set_project_data({'settings': 'settings'})

    def test_get(self):
        self.setSettings({'key': 'value'})

        self.assertEqual(settings.get('key'), 'value')


@unittest.skip
class InvalidProjectPluginSettingsTestCase(SublimeWindowTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.window.set_project_data(
            {'settings': {settings.PROJECT_SETTINGS_KEY: 'settings'}}
        )

    def test_get(self):
        self.setSettings({'key': 'value'})

        self.assertEqual(settings.get('key'), 'value')
