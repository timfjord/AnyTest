from . import panel


class Output(panel.Output):
    name = 'terminus'

    def sublime_command(self):
        return 'terminus_exec'

    def options(self):
        return dict(
            super().options(),
            focus=self.settings('focus_on_run', type=bool, default=False),
        )
