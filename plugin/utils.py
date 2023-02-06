import re
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


def to_unpackable(val):
    return val if isinstance(val, list) or isinstance(val, tuple) else (val,)


def match_patterns(string, patterns):
    for pattern in patterns:
        if isinstance(pattern, tuple):
            pattern, name = pattern
        else:
            name = None

        match = re.search(pattern, string)
        if match is not None:
            return match.group(1), name

    return None, None
