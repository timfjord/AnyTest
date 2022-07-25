import sublime

from . import settings
from .mixins import WindowMixin


class ViewCallbacks(WindowMixin):
    SCROLL_TO_VIEW_TIMEOUT = 750

    def __init__(self, view):
        self.view = view
        self.is_editable = bool(self.view.file_name())
        self._prev_visible_region = None

    @property
    def window(self):
        return self.view.window()

    def save(self):
        if settings.get('save_all_files_on_run'):
            self.run_command('save_all')
        elif settings.get('save_current_file_on_run') and self.is_editable:
            self.run_command('save')

    def scroll_to_view(self):
        if (
            not settings.get('scroll_to_view_on_run')
            or not self.is_editable
            or self._prev_visible_region is None
        ):
            return

        overlaid_region = sublime.Region(
            self.view.visible_region().end() + 1, self._prev_visible_region.end()
        )

        if len(self.view.sel()) < 1:
            return

        if not overlaid_region.contains(self.view.sel()[-1].end()):
            return

        diff = -len(self.view.lines(overlaid_region))
        self.view.run_command('scroll_lines', {'amount': float(diff)})

    def run(self):
        self.save()

        self._prev_visible_region = self.view.visible_region()
        sublime.set_timeout(self.scroll_to_view, self.SCROLL_TO_VIEW_TIMEOUT)
