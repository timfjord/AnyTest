import logging

from .plugin import settings

DEFAULT_LOG_LEVEL = logging.WARNING
DEFAULT_LOG_LEVEL_NAME = logging.getLevelName(DEFAULT_LOG_LEVEL)
EVENT_LEVEL = logging.INFO

package_logger = logging.getLogger(__package__)
package_logger.propagate = False
package_logger.setLevel(DEFAULT_LOG_LEVEL)

if not package_logger.hasHandlers():
    handler = logging.StreamHandler()

    formatter = logging.Formatter(fmt="AnyTest({levelname}): {message}", style='{')
    handler.setFormatter(formatter)

    package_logger.addHandler(handler)


def plugin_loaded():
    def on_settings_reload():
        if package_logger is None:
            return

        cur_log_level = package_logger.getEffectiveLevel()
        cur_log_level_name = logging.getLevelName(cur_log_level)
        new_log_level_name = settings.get(
            'log_level', type=str, default=DEFAULT_LOG_LEVEL_NAME
        ).upper()
        new_log_level = getattr(logging, new_log_level_name, DEFAULT_LOG_LEVEL)

        if new_log_level_name == cur_log_level_name:
            return

        if cur_log_level > EVENT_LEVEL and new_log_level <= EVENT_LEVEL:
            # Only set level before emitting log event if it would not be seen otherwise
            package_logger.setLevel(new_log_level)
        package_logger.log(
            EVENT_LEVEL,
            "Changing log level from %r to %r",
            cur_log_level_name,
            new_log_level_name,
        )
        package_logger.setLevel(new_log_level)  # Just set it again to be sure

    settings.all().add_on_change(__name__, on_settings_reload)
    on_settings_reload()  # trigger on initial settings load, too
    package_logger.error('NO DUP')


def plugin_unloaded():
    settings.all().clear_on_change(__name__)
