from . import panel


class Output(panel.Output):
    PANEL_NAME = 'AnyTest'
    TAG = 'any-test'

    name = 'terminus'

    def panel_command(self):
        return 'terminus_open'

    def options(self):
        options = super().options()
        options.pop('encoding', None)

        options['auto_close'] = False
        options['cancellable'] = True
        options['tag'] = self.TAG
        if self.settings('run_in_view', type=bool, default=False):
            options['title'] = 'Running {} {} tests'.format(
                self.test_framework.language, self.test_framework.framework
            )
            options['pre_window_hooks'] = self.settings(
                'pre_window_hooks', type=list, default=[]
            )
            options['post_window_hooks'] = self.settings(
                'post_window_hooks', type=list, default=[]
            )
            options['post_view_hooks'] = self.settings(
                'post_view_hooks', type=list, default=[]
            )
        else:
            options['focus'] = self.settings('focus_on_run', type=bool, default=False)
            options['panel_name'] = self.PANEL_NAME

        return options
