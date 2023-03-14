from AnyTest.plugin.runners import Runner as BaseRunner
from AnyTest.tests import SublimeWindowTestCase


class DummuRunner(BaseRunner):
    name = "dummy"

    def run(self):
        pass


def build_runner(dir="dir", file="file"):
    return DummuRunner(
        "scope", "cmd", dir, file, "line", "language", "framework", {}, False
    )


class BaseRunnerTestCase(SublimeWindowTestCase):
    def test_init(self):
        runner = build_runner()

        self.assertEqual(runner.scope, "scope")
        self.assertEqual(runner.cmd, "cmd")
        self.assertEqual(runner.dir, "dir")
        self.assertEqual(runner.file, "file")
        self.assertEqual(runner.line, "line")
        self.assertEqual(runner.language, "language")
        self.assertEqual(runner.framework, "framework")
        self.assertEqual(runner.options, {})

        self.assertEqual(
            runner.to_dict(),
            {
                "scope": "scope",
                "cmd": "cmd",
                "dir": "dir",
                "file": "file",
                "line": "line",
                "language": "language",
                "framework": "framework",
                "options": {},
                "modified": False,
            },
        )

    def test_settings(self):
        self.assertIsNone(DummuRunner.settings("something"))

        self.setSettings({"runner.dummy.something": "value"})

        self.assertEqual(DummuRunner.settings("something"), "value")

    def test_settings_raise_error_when_no_name(self):
        with self.assertRaises(NotImplementedError):
            BaseRunner.settings("something")

    def test_relpath(self):
        runner = build_runner("/dir", "/dir/file")

        self.assertEqual(runner.relpath, "file")
