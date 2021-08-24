# --- Clear module cache ---
# Clear module cache to force reloading all modules of this package.
# See https://github.com/emmetio/sublime-text-plugin/issues/35
import sys

prefix = __package__ + '.'  # don't clear the base package
for module_name in [
    module_name
    for module_name in sys.modules
    if module_name.startswith(prefix) and module_name != __name__
]:
    del sys.modules[module_name]
# --- Clear module cache ---


import sublime_plugin  # noqa: E402

from .plugin import Context, Error, Runner, logger  # noqa: E402


class AnyTestRunCommand(sublime_plugin.TextCommand):
    def run(self, edit, scope='file'):
        try:
            context = Context.find(self.view)

            Runner(context).run(scope)
        except Error as e:
            logger.log(e)
