import shlex


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


def regex(string):
    return string.translate(REGEXP_ESCAPE_TRANSLATION_TABLE)


def shell(string):
    return shlex.quote(string).translate(SHELL_ESCAPE_TRANSLATION_TABLE)
