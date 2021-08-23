import sublime


BASE_NAME = 'AnyTest.sublime-settings'


def get(key, type=None, default=None):
    if not isinstance(key, str):
        key = '.'.join(key)

    value = sublime.load_settings(BASE_NAME).get(key, default=default)

    if type is not None and not isinstance(value, type):
        return None

    return value
