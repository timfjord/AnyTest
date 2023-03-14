# --- Clear module cache ---
# Clear module cache to force reloading all modules of this package.
# See https://github.com/emmetio/sublime-text-plugin/issues/35
import sys

prefix = __package__ + "."  # don't clear the base package
for module_name in [
    module_name
    for module_name in sys.modules
    if module_name.startswith(prefix) and module_name != __name__
]:
    del sys.modules[module_name]
# --- Clear module cache ---


import sublime_plugin  # noqa: E402

from .plugin import SCOPE_LAST, Plugin  # noqa: E402


class AnyTestRunCommand(sublime_plugin.TextCommand):
    def run(self, _, scope="file", edit=False, select=False):
        plugin = Plugin(self.view)

        if select and scope != SCOPE_LAST:
            plugin.select_test_framework(scope, edit)
        else:
            plugin.run_test(scope, edit)


class AnyTestShowLastOutputCommand(sublime_plugin.ApplicationCommand):
    def run(self, focus=True):
        Plugin.show_last_output(focus=focus)


class AnyTestEditLastCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        Plugin.edit_last()


class AnyTestShowHistoryCommand(sublime_plugin.TextCommand):
    def run(self, _):
        Plugin(self.view).show_history()


class AnyTestClearHistoryCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        Plugin.clear_history()
