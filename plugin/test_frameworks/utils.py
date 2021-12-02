import shlex
from distutils import spawn


REGEXP_ESCAPE_TRANSLATION_TABLE = str.maketrans(
    {
        '?': r'\?',
        '+': r'\+',
        '*': r'\*',
        '\\': r'\\',
        '^': r'\^',
        '$': r'\$',
        '.': r'\.',
        '|': r'\|',
        '{': r'\{',
        '}': r'\}',
        '[': r'\[',
        ']': r'\]',
        '(': r'\(',
        ')': r'\)',
    }
)
SHELL_ESCAPE_TRANSLATION_TABLE = str.maketrans(
    {
        '$': r'\$',  # to avoid issues with the $ symbol in terminus
    }
)


def escape_regex(string):
    return string.translate(REGEXP_ESCAPE_TRANSLATION_TABLE)


def escape_shell(string):
    return shlex.quote(string).translate(SHELL_ESCAPE_TRANSLATION_TABLE)


def is_executable(name):
    return bool(spawn.find_executable(name))
