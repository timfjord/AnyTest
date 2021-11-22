from unittest import TestCase

import sublime

from AnyTest.plugin import settings


class SublimeViewTestCase(TestCase):
    def setUp(self):
        self.view = sublime.active_window().new_file()
        sublime.load_settings('Preferences.sublime-settings').set(
            'close_windows_when_empty', False
        )

        self.settings = sublime.load_settings(settings.BASE_NAME)
        self._setting_keys = set()

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

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
