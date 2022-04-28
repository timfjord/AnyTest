import os
import re

from .. import rust, utils


class TestFramework(rust.TestFramework):
    NEAREST_SEPARATOR = '::'
    MANIFEST_FILE = 'Cargo.toml'

    framework = 'cargotest'
    pattern = r'.rs$'

    test_patterns = (r'(#\[(?:\w+::|rs)?test)',)
    namespace_patterns = (r'mod (tests?)',)

    forward_test_patterns = (r'\s*(?:async )?fn\s+(\w+)',)

    def build_file_position_args(self):
        path, _ = os.path.splitext(self.context.file.relpath)
        modules = path.split(os.sep)

        if re.search(r'^(main|lib|mod)$', modules[-1]):
            modules.pop()

        args = []
        for i in range(len(modules) - 1, 0, -1):
            parts = modules[:i] + [self.MANIFEST_FILE]
            if self.file(*parts).exists():
                args += ['--package', modules[i - 1]]
                modules = modules[i:]
                break

        if modules[0] == 'tests' and len(modules) == 2 or len(modules) <= 1:
            return args

        namespace = self.NEAREST_SEPARATOR.join(modules[1:] + [''])
        return args + [utils.escape_shell(namespace)]

    def build_line_position_args(self):
        file_args = self.build_file_position_args()
        nearest = self.find_nearest()

        if not bool(nearest.tests) or not re.search(r'#\[.*', nearest.tests[0]):
            return file_args

        forward_nearest = self.context.find_nearest(
            self.forward_test_patterns, from_line=nearest.line, to_line='current'
        )
        test_name = self.NEAREST_SEPARATOR.join(
            nearest.namespaces[0:1] + forward_nearest.tests[0:1]
        )
        file_namespace = file_args.pop() if bool(file_args) else ''

        return file_args + [
            file_namespace + utils.escape_regex(test_name),
            '--',
            '--exact',
        ]
