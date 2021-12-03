import sublime


BASE_NAME = 'AnyTest.sublime-settings'
PROJECT_SETTINGS_KEY = 'AnyTest'

_project_settings = None


def _ensure_dict(d):
    return d if isinstance(d, dict) else {}


def reload_project_settings():
    global _project_settings
    _project_settings = None


def get_project_settings():
    global _project_settings

    if _project_settings is None:
        # fmt: off
        _project_settings = _ensure_dict(
            _ensure_dict(
                _ensure_dict(
                    sublime.active_window().project_data()
                ).get('settings', {})
            ).get(PROJECT_SETTINGS_KEY, {})
        )
        # fmt: on

    return _project_settings


def get(key, type=None, default=None):
    project_settings = get_project_settings()

    if not isinstance(key, str):
        key = '.'.join(key)

    value = (
        project_settings.get(key, default)
        if key in project_settings
        else sublime.load_settings(BASE_NAME).get(key, default=default)
    )

    if type is not None and not isinstance(value, type):
        return None

    return value
