import logging

import sublime

from .cache import cache

BASE_NAME = "AnyTest.sublime-settings"
PROJECT_SETTINGS_KEY = "AnyTest"

logger = logging.getLogger(__name__)


def _ensure_dict(d):
    return d if isinstance(d, dict) else {}


# window_cache('project_settings')
@cache
def project_settings():
    # fmt: off
    return _ensure_dict(
        _ensure_dict(
            _ensure_dict(
                sublime.active_window().project_data()
            ).get("settings", {}),
        ).get(PROJECT_SETTINGS_KEY, {})
    )
    # fmt: on


def settings():
    return sublime.load_settings(BASE_NAME)


def get(key, type=None, default=None):
    if not isinstance(key, str):
        key = ".".join(key)

    value = (
        project_settings().get(key, default)
        if key in project_settings()
        else settings().get(key, default=default)
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
