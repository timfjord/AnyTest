import logging
from functools import wraps

logger = logging.getLogger(__name__)


def handle_errors(func):
    @wraps(func)
    def handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Error as e:
            logger.error(e)

    return handler


class Error(Exception):
    DEFAULT_MESSAGE = ''

    def __init__(self, *args, **kwargs):
        if not args and bool(self.DEFAULT_MESSAGE):
            args = (self.DEFAULT_MESSAGE,)

        super().__init__(*args, **kwargs)


class EmptyHistory(Error):
    DEFAULT_MESSAGE = 'No tests were run so far in this window'


class FrameworkNotFound(Error):
    DEFAULT_MESSAGE = "Couldn't find the right test framework"


class InvalidContext(Error):
    DEFAULT_MESSAGE = 'Test context is invalid'
