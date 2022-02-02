import sublime


class WindowMixin:
    @property
    def window(self):
        return sublime.active_window()

    def run_command(self, *args, **kwargs):
        self.window.run_command(*args, **kwargs)
