from AnyTest.tests import SublimeWindowTestCase
from AnyTest.plugin.test_frameworks import TestFramework
from AnyTest.plugin.test_frameworks.mixins import IsConfigurableMixin


class TFBase(TestFramework):
    @classmethod
    def is_suitable_for(cls, _):
        return True


class TF(IsConfigurableMixin, TFBase):
    language = '_lng'
    framework = '_frm'

    @classmethod
    def is_configurable_fallback(cls, file):
        return file == 'ACTIVATE'


class IsConfigurableMixinTestCase(SublimeWindowTestCase):
    def test_is_the_only_available_default(self):
        self.assertFalse(TF.is_the_only_available())

        self.setSettings({'test_frameworks': {'_lng': '_frm'}})

        self.assertTrue(TF.is_the_only_available())

    def test_is_suitable_for_default(self):
        self.assertFalse(TF.is_suitable_for('_file'))

    def test_is_suitable_for_the_only_available(self):
        self.setSettings({'test_frameworks': {'_lng': '_frm'}})

        self.assertTrue(TF.is_suitable_for('_file'))

    def test_is_suitable_for_with_configured(self):
        self.setSettings({'_lng.test_framework': '_frm'})

        self.assertTrue(TF.is_suitable_for('_file'))

    def test_is_suitable_for_with_other_configured(self):
        self.setSettings({'_lng.test_framework': '_other_frm'})

        self.assertFalse(TF.is_suitable_for('_file'))

    def test_is_suitable_for_with_fallback(self):
        """
        To avoid mocking the `is_configurable_fallback` fallback
        it returns True only when the first argument is equal 'ACTIVATE'
        """
        self.assertTrue(TF.is_suitable_for('ACTIVATE'))
