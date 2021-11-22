from AnyTest.plugin import settings
from AnyTest.tests import SublimeViewTestCase


class SettingsTestCase(SublimeViewTestCase):
    def test_unknown(self):
        self.assertIsNone(settings.get('unknown'))

    def test_passing_an_iterator(self):
        self.setSettings({'key.subkey': 'value'})

        self.assertEqual(settings.get(('key', 'subkey')), 'value')

    def test_default(self):
        self.assertEqual(settings.get('unknown', default='value'), 'value')

    def test_typing(self):
        self.setSettings({'key': 'value'})

        self.assertEqual(settings.get('key', type=str), 'value')
        self.assertIsNone(settings.get('key', type=bool))
