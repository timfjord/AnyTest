from functools import wraps

from . import logger


def handle_errors(func):
    @wraps(func)
    def handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Error as e:
            logger.log(e)

    return handler


class Error(Exception):
    DEFAULT_MESSAGE = ''

    def __init__(self, *args, **kwargs):
        if not args and bool(self.DEFAULT_MESSAGE):
            args = (self.DEFAULT_MESSAGE,)

        super().__init__(*args, **kwargs)


class NoLastCommand(Error):
    DEFAULT_MESSAGE = 'No tests were run so far'


class FrameworkNotFound(Error):
    DEFAULT_MESSAGE = "Couldn't find the right test framework"


class InvalidOutputCommand(Error):
    DEFAULT_MESSAGE = 'Output command is not set'


class InvalidContext(Error):
    DEFAULT_MESSAGE = 'Test context is invalid'


class OutputNotFound(Error):
    DEFAULT_MESSAGE = "Couldn't find the right output"
