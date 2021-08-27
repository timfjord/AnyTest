from collections import namedtuple

from . import errors, outputs


class Command(
    namedtuple('Command', 'command, directory, file, line, language, framework')
):
    __slots__ = ()
    _last = None

    @classmethod
    def from_framework(cls, framework, scope):
        return (
            cls(
                ' '.join(framework.build_command(scope)),
                framework.context.directory(),
                framework.context.file(),
                framework.context.line(),
                framework.language,
                framework.framework,
            ),
            framework.__class__,
        )

    @classmethod
    def last(cls):
        if cls._last is None:
            raise errors.NoLastCommand

        return (cls(**cls._last), None)

    def run(self, test_framework=None):
        outputs.build(self, test_framework=test_framework)

        self.save_last_command()

    def save_last_command(self):
        self.__class__._last = self._asdict()
