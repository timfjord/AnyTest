from ..utils import replace
from .command import Runner as CommandRunner


class Runner(CommandRunner):
    PANEL_NAME = 'AnyTest'
    TAG = 'any-test'
    COMMAND_NAME = 'terminus_open'

    name = 'terminus'
    panel_name = 'output.{}'.format(PANEL_NAME)

    def get_panel_name(self):
        super().get_panel_name()  # to clean up options
        return self.__class__.panel_name

    def get_command_name(self):
        super().get_command_name()  # to clean up options
        return self.COMMAND_NAME

    def get_command_options(self):
        return dict(super().get_command_options(), **{'tag': self.TAG})

    class Builder(CommandRunner.Builder):
        def build_cmd(self):
            return replace(
                super().build_cmd(),
                # the `$` symbol in terminus needs to be escaped
                (r'(?<!\\)(\$)', r'\\\1'),
                # this replacement is here because some test frameworks (e.g. gotest)
                # that require double escaping of the regexp characters
                # causes issues with the terminus, as it requires `\\\^\\\$\\\|\\\(\\\)` symbols to
                # be `\\\\\^\\\\\$\\\\\|\\\\\(\\\\\)`
                # if this global rule break some test frameworks then it needs to be triggered by
                # the required test frameworks (for example via #get_options method)
                (r'(\\\\\\[\^\$\|\(\)])', r'\\\\\1'),
            )

        def build_options(self):
            options = super().build_options()
            options.pop('encoding', None)
            options.pop('file_regex', None)

            options['auto_close'] = False
            options['cancellable'] = True

            if Runner.settings('run_in_view', type=bool, default=False):
                options['title'] = 'Running {} {} tests'.format(
                    self.test_framework.language, self.test_framework.framework
                )
                options['pre_window_hooks'] = Runner.settings(
                    'pre_window_hooks', type=list, default=[]
                )
                options['post_window_hooks'] = Runner.settings(
                    'post_window_hooks', type=list, default=[]
                )
                options['post_view_hooks'] = Runner.settings(
                    'post_view_hooks', type=list, default=[]
                )
            else:
                options['focus'] = Runner.settings(
                    'focus_on_run', type=bool, default=False
                )
                options['panel_name'] = Runner.PANEL_NAME

            return options
