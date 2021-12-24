from pathlib import Path

import sublime

from unittesting import DeferrableTestCase

from AnyTest.plugin import settings
from AnyTest.plugin.command import Command
from AnyTest.plugin.errors import NoLastCommand
from AnyTest.plugin.test_frameworks import TestFramework


FIXTURES_PATH = Path(__file__).parent.joinpath('fixtures')


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
    def setUp(self):
        super().setUp()

        self.view = self.buildView()

    def buildView(self):
        return self.window.new_file()

    def focusView(self):
        self.window.focus_view(self.view)

    def isViewLoaded(self):
        return not self.view.is_loading()

    def tearDown(self):
        if not self.view:
            return

        self.view.set_scratch(True)
        self.view.close()

    def setText(self, string):
        self.view.run_command('insert', {'characters': string})

    def getRow(self, row):
        return self.view.substr(self.view.line(self.view.text_point(row, 0)))

    def gotoLine(self, line):
        self.focusView()
        self.view.run_command('goto_line', {'line': line})

        return line

    def assertLastCommand(self, command):
        try:
            last_command = Command.last().command
        except NoLastCommand:
            last_command = ''

        self.assertEqual(last_command, command)


class SublimeFileTestCase(SublimeViewTestCase):
    def buildView(self):
        pass

    def Test(self, folder=None, file=None, line=None):
        scope = TestFramework.SCOPE_SUITE

        if folder is not None:
            path = FIXTURES_PATH.joinpath(folder)
            self.window.set_project_data({'folders': [{'path': str(path)}]})

            if file is not None:
                scope = TestFramework.SCOPE_FILE
                file_path = path.joinpath(file)
                self.view = self.window.open_file(str(file_path))

                yield self.isViewLoaded

        if line is not None:
            scope = TestFramework.SCOPE_LINE
            self.gotoLine(line)

            yield

        self.view.run_command('any_test_run', {'scope': scope})
