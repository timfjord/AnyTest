import logging

import sublime

BASE_NAME = 'AnyTest.sublime-settings'
PROJECT_SETTINGS_KEY = 'AnyTest'

logger = logging.getLogger(__name__)

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


def all():
    return sublime.load_settings(BASE_NAME)


def get(key, type=None, default=None):
    project_settings = get_project_settings()

    if not isinstance(key, str):
        key = '.'.join(key)

    value = (
        project_settings.get(key, default)
        if key in project_settings
        else all().get(key, default=default)
    )

    if type is not None and not isinstance(value, type):
        logger.info(
            "type doesn't match: key: '%s', value: '%s', expected type: '%s'",
            key,
            value,
            type.__name__,
        )
        return None

    return value
