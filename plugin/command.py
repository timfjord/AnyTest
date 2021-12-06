from collections import namedtuple

from . import errors


class Command(
    namedtuple('Command', 'command, directory, file, line, language, framework')
):
    __slots__ = ()
    _last = None

    @classmethod
    def build(cls, framework, scope):
        return cls(
            ' '.join(framework.build_command(scope)),
            framework.context.root.path,
            framework.context.file.path,
            framework.context.sel_line(),
            framework.language,
            framework.framework,
        )

    @classmethod
    def last(cls):
        if cls._last is None:
            raise errors.NoLastCommand

        return cls(**cls._last)

    def save(self):
        self.__class__._last = self._asdict()
