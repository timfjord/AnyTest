import re
from distutils import spawn
from functools import reduce

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


def escape_regex(string):
    """
    Switch to re.escape once upgrade to Python 3.8 as it doesn't escape the / symbol
    """
    return string.translate(REGEXP_ESCAPE_TRANSLATION_TABLE)


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


def replace(string, *replacements):
    return reduce(
        lambda value, args: re.sub(args[0], args[1], value),
        replacements,
        string,
    )
