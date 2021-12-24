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


def escape_shell(string, quote=True):
    if quote:
        string = shlex.quote(string)

    return string.translate(SHELL_ESCAPE_TRANSLATION_TABLE)


def escape(string, symbols):
    for char in symbols:
        string = string.replace(char, '\\{}'.format(char))

    return string


def is_executable(name):
    return bool(spawn.find_executable(name))
