from functools import lru_cache

from . import command


class Runner(command.Runner):
    PANEL_NAME = 'AnyTest'
    TAG = 'any-test'

    name = 'terminus'

    def command_name(self):
        return 'terminus_open'

    @lru_cache(maxsize=None)
    def command_options(self):
        options = super().command_options()
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
