import os

import sublime

from unittesting import DeferrableTestCase

from AnyTest.plugin import settings
from AnyTest.plugin.command import Command
from AnyTest.plugin.errors import NoLastCommand
from AnyTest.plugin.test_frameworks import TestFramework


FIXTURES_PATH = os.path.join(os.path.dirname(__file__), 'fixtures')


class SublimeWindowTestCase(DeferrableTestCase):
    @classmethod
    def setUpClass(cls):
        sublime.run_command('new_window')
        cls.window = sublime.active_window()
        cls.window.set_project_data({'settings': {settings.PROJECT_SETTINGS_KEY: {}}})

        sublime.load_settings('Preferences.sublime-settings').set(
            'close_windows_when_empty', False
        )

        settings.reload_project_settings()

    @classmethod
    def tearDownClass(cls):
        cls.window.run_command('close_window')

    def setUp(self):
        self.settings = sublime.load_settings(settings.BASE_NAME)
        self._setting_keys = set()

        self.setSettings({'output': 'console'})

    def tearDown(self):
        for key in self._setting_keys:
            self.settings.erase(key)

    def setSettings(self, pairs):
        self._setting_keys |= set(pairs.keys())

        for key, value in pairs.items():
            self.settings.set(key, value)


class SublimeViewTestCase(SublimeWindowTestCase):
    new_file = False

    def setUp(self):
        super().setUp()

        self.view = self.window.new_file() if self.new_file else None

    def focusView(self):
        if not self.view:
            return

        self.window.focus_view(self.view)

    def isViewLoaded(self):
        if not self.view:
            return True

        return not self.view.is_loading()

    def tearDown(self):
        if not self.view:
            return

        self.view.set_scratch(True)
        self.view.close()

    def gotoLine(self, line):
        if not self.view:
            return

        self.focusView()
        self.view.run_command('goto_line', {'line': line})

        return line

    def _testLine(self, line):
        if not self.view:
            return

        self.gotoLine(line)
        self.view.run_command('any_test_run', {'scope': TestFramework.SCOPE_LINE})

    def _testFile(self, folder, file, line=None, scope=None):
        test_scope = scope if scope is not None else TestFramework.SCOPE_FILE

        if not isinstance(folder, list) and not isinstance(folder, tuple):
            folder = (folder,)
        path = os.path.join(FIXTURES_PATH, *folder)
        self.window.set_project_data({'folders': [{'path': path}]})

        file_path = os.path.join(path, file)
        self.view = self.window.open_file(file_path)

        yield self.isViewLoaded

        if line is not None:
            self.gotoLine(line)

            if scope is None:
                test_scope = TestFramework.SCOPE_LINE

        self.view.run_command('any_test_run', {'scope': test_scope})

    def _testSuite(self, folder, file):
        yield from self._testFile(folder, file, scope=TestFramework.SCOPE_SUITE)

    def assertLastCommand(self, command):
        try:
            last_command = Command.last().command
        except NoLastCommand:
            last_command = ''

        self.assertEqual(last_command, command)
