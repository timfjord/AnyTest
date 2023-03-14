import types

from AnyTest.plugin.errors import EmptyHistory
from AnyTest.plugin.history import History
from AnyTest.plugin.runners.command import Runner as CommandRunner
from AnyTest.tests import SublimeWindowTestCase


def build_runner(cmd, dir="dir", modified=False):
    return CommandRunner(
        scope="scope",
        cmd=cmd,
        dir=dir,
        file="file",
        line="line",
        language="language",
        framework="framework",
        options="options",
        modified=modified,
    )


class SettingsTestCase(SublimeWindowTestCase):
    def setUp(self):
        super().setUp()

        self.history = History(self.window)
        self.history.clear()

    def test_items(self):
        self.history.items = ["item1", "item2"]

        self.assertEqual(self.history.items, ["item1", "item2"])

    def test_add_and_clear(self):
        runner1 = build_runner("cmd1")
        runner2 = build_runner("cmd2")
        runner3 = build_runner("cmd1", modified=True)

        self.history.add(runner1)
        self.assertEqual(
            self.history.items,
            [{"runner": "command", "kwargs": runner1.to_dict()}],
        )

        self.history.add(runner2)
        self.assertEqual(
            self.history.items,
            [
                {"runner": "command", "kwargs": runner2.to_dict()},
                {"runner": "command", "kwargs": runner1.to_dict()},
            ],
        )

        self.history.add(runner1)
        self.assertEqual(
            self.history.items,
            [
                {"runner": "command", "kwargs": runner1.to_dict()},
                {"runner": "command", "kwargs": runner2.to_dict()},
            ],
        )

        self.history.add(runner3)
        self.assertEqual(
            self.history.items,
            [
                {"runner": "command", "kwargs": runner3.to_dict()},
                {"runner": "command", "kwargs": runner2.to_dict()},
            ],
        )

        self.history.clear()
        self.assertEqual(self.history.items, [])

    def test_add_same_cmd_different_dir(self):
        runner1 = build_runner("cmd", dir="dir1")
        runner2 = build_runner("cmd", dir="dir2")

        self.history.add(runner1)
        self.history.add(runner2)
        self.assertEqual(
            self.history.items,
            [
                {"runner": "command", "kwargs": runner2.to_dict()},
                {"runner": "command", "kwargs": runner1.to_dict()},
            ],
        )

    def test_add_more_than_10(self):
        for i in range(History.MAX_ITEMS + 1):
            self.history.add(build_runner("cmd{}".format(i)))

        self.assertEqual(len(self.history.items), History.MAX_ITEMS)

    def test_runners(self):
        runner = build_runner("cmd")
        self.history.add(runner)

        self.assertIsInstance(self.history.runners, types.GeneratorType)

        runners = list(self.history.runners)
        self.assertEqual(runners, [runner])

    def test_last(self):
        with self.assertRaises(EmptyHistory):
            self.history.last()

        runner = build_runner("cmd")
        self.history.add(runner)

        self.assertEqual(self.history.last(), runner)
