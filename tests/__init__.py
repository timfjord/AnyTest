import os

import sublime

from unittesting import DeferrableTestCase

from AnyTest.plugin import settings
from AnyTest.plugin.test_frameworks import TestFramework
from AnyTest.plugin.runners.tests import last_command


FIXTURES_PATH = os.path.join(os.path.dirname(__file__), 'fixtures')


def to_iter(val):
    return val if isinstance(val, list) or isinstance(val, tuple) else (val,)


class SublimeWindowTestCase(DeferrableTestCase):
    _currentFolder = None

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

    @classmethod
    def openFolder(cls, *paths):
        cls._currentFolder = os.path.join(FIXTURES_PATH, *paths)
        cls.window.set_project_data({'folders': [{'path': cls._currentFolder}]})

    def setUp(self):
        self.settings = sublime.load_settings(settings.BASE_NAME)
        self._setting_keys = set()

        self.setSettings({'runner': 'tests'})

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
        super().tearDown()

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

    def _testFile(self, file, line=None, scope=None):
        test_scope = scope if scope is not None else TestFramework.SCOPE_FILE

        if self._currentFolder is None:
            raise ValueError('Call cls.openFolder in the setUpClass callback')

        file_path = os.path.join(self._currentFolder, *to_iter(file))
        self.view = self.window.open_file(file_path)

        yield self.isViewLoaded

        if line is not None:
            self.gotoLine(line)

            if scope is None:
                test_scope = TestFramework.SCOPE_LINE

        self.view.run_command('any_test_run', {'scope': test_scope})

    def _testSuite(self, file):
        yield from self._testFile(file, scope=TestFramework.SCOPE_SUITE)

    def assertLastCommand(self, command):
        self.assertEqual(last_command(self.view), command)
