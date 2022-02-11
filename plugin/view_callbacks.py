import sublime

from . import settings
from .mixins import WindowMixin


class ViewCallbacks(WindowMixin):
    SCROLL_TO_VIEW_TIMEOUT = 750

    def __init__(self, view):
        self.view = view
        self.is_editable = bool(self.view.file_name())
        self._num_of_visible_lines = None

    @property
    def window(self):
        return self.view.window()

    def num_of_visible_lines(self):
        return len(self.view.lines(self.view.visible_region()))

    def save(self):
        if settings.get('save_all_files_on_run'):
            self.run_command('save_all')
        elif settings.get('save_current_file_on_run') and self.is_editable:
            self.run_command('save')

    def scroll_to_view(self):
        if (
            settings.get('scroll_to_view_on_run')
            and self.is_editable
            and self._num_of_visible_lines is not None
        ):
            diff = self.num_of_visible_lines() - self._num_of_visible_lines
            self.view.run_command('scroll_lines', args={'amount': float(diff)})

    def run(self):
        self.save()

        self._num_of_visible_lines = self.num_of_visible_lines()
        sublime.set_timeout(self.scroll_to_view, self.SCROLL_TO_VIEW_TIMEOUT)
