from functools import lru_cache

from .. import elixir


class TestFramework(elixir.TestFramework):
    framework = 'exunit'
    pattern = r'_test\.exs$'

    @lru_cache(maxsize=None)
    def is_mix(self):
        return self.file('mix.exs').exists()

    def build_executable(self):
        if self.is_mix():
            return ['mix', 'test']

        return ['elixir']

    def build_suite_position_args(self):
        if self.is_mix():
            return []

        return ['*.exs']

    def build_file_position_args(self):
        return [self.context.file.relpath]

    def build_line_position_args(self):
        file_args = self.build_file_position_args()
        sel_line = self.context.sel_line()

        if not self.is_mix() or sel_line < 2:
            return file_args

        return ['{}:{}'.format(self.context.file.relpath, sel_line)]
