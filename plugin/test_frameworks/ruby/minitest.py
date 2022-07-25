import re
from functools import lru_cache

from .. import ruby, utils


class TestFramework(ruby.TestFramework):
    NAMESPEACE_SEPARATOR = '::'
    METHOD_SEPARATOR = '#'

    framework = 'minitest'
    pattern = r'(((^|/|\\)test_[^/\\]+)|_test)(?<!spec).rb$'

    @classmethod
    def is_suitable_for(cls, file):
        return super().is_suitable_for(file) and not cls.settings('use_m', type=bool)

    @classmethod
    def test_folder(cls):
        return cls.settings('test_folder', type=str, fallback=False)

    @classmethod
    def test_file_pattern(cls):
        return cls.settings(
            'file_pattern',
            type=str,
            fallback=False,
        )

    @lru_cache(maxsize=None)
    def rakefile(self):
        return self.file('Rakefile')

    @lru_cache(maxsize=None)
    def use_rake(self):
        return (
            self.rakefile().exists()
            and self.rakefile().contains('Rake::TestTask')
            or self.file('bin', 'rails').exists()
        )

    @lru_cache(maxsize=None)
    def bin(self):
        return self.file('bin', 'rake')

    def build_executable(self):
        if self.use_rake():
            return self._build_executable(
                ['rake', 'test'], zeus=True, binstubs=['test']
            )

        return self._build_executable(['ruby', '-I{}'.format(self.test_folder())])

    def build_file_position_args(self):
        if self.use_rake():
            return ['TEST="{}"'.format(utils.escape(self.context.file.relpath, '"'))]
        else:
            return [self.context.file.relpath]

    def build_line_position_args(self):
        file_args = self.build_file_position_args()
        nearest_args = []
        nearest = self.build_nearest()

        if bool(nearest):
            name = "/{}/".format(nearest)

            if self.use_rake():
                nearest_args = ['TESTOPTS="--name={}"'.format(utils.escape(name, '"`'))]
            else:
                nearest_args = ['--name', name]

        return file_args + nearest_args

    def build_nearest(self):
        nearest = self.find_nearest()
        namespace = (
            [self.NAMESPEACE_SEPARATOR.join(nearest.namespaces)]
            if bool(nearest.namespaces)
            else []
        )
        test = []

        if bool(nearest.tests):
            test_name = utils.escape_regex('{}$'.format(nearest.tests[0]))
            syntax = nearest.names[0]

            if syntax == 'rails':
                test_name = 'test_{}'.format(re.sub(r'\s+', '_', test_name))
            elif syntax == 'spec':
                test_name = r'test_\d+_{}'.format(test_name)

            test = [test_name]

        return self.METHOD_SEPARATOR.join(namespace + test)

    def build_command(self, scope):
        command = super().build_command(scope)

        if scope != self.SCOPE_SUITE:
            return command

        # building a command like find `test -name "*_test.rb" -exec bundle exec ruby -Itest {} +`
        # as a workaround for globstar in Bash, see https://github.com/randy3k/Terminus/issues/332
        return (
            [
                'find',
                utils.escape_shell(self.test_folder(), quote=False),
                '-name',
                utils.escape_shell(self.test_file_pattern(), quote=False),
                '-exec',
            ]
            + command
            + ['{}', '+']
        )
