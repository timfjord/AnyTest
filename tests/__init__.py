from unittest import TestCase

import sublime

from AnyTest.plugin import settings


class SublimeViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        sublime.run_command('new_window')
        cls.window = sublime.active_window()
        cls.window.set_project_data({'settings': {settings.PROJECT_SETTINGS_KEY: {}}})

        sublime.load_settings('Preferences.sublime-settings').set(
            'close_windows_when_empty', False
        )

    @classmethod
    def tearDownClass(cls):
        cls.window.run_command('close_window')

    def setUp(self):
        self.view = view = self.window.new_file()
        self.addCleanup(self.close_view, view)

        self.settings = sublime.load_settings(settings.BASE_NAME)
        self._setting_keys = set()

    def close_view(self, view):
        if not view:
            return

        view.set_scratch(True)
        view.close()

    def tearDown(self):
        for key in self._setting_keys:
            self.settings.erase(key)

    def setText(self, string):
        self.view.run_command('insert', {'characters': string})

    def getRow(self, row):
        return self.view.substr(self.view.line(self.view.text_point(row, 0)))

    def setSettings(self, pairs):
        self._setting_keys |= set(pairs.keys())

        for key, value in pairs.items():
            self.settings.set(key, value)
