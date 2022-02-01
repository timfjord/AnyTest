from .utils import to_unpackable
from .. import settings


class IsConfigurableMixin:
    @classmethod
    def is_the_only_available(cls):
        available_frameworks = tuple(
            to_unpackable(
                settings.get(
                    'test_frameworks',
                    type=dict,
                    default={},
                ).get(cls.language, ())
            )
        )

        return available_frameworks == (cls.framework,)

    @classmethod
    def is_suitable_for(cls, file):
        if not super().is_suitable_for(file):
            return False

        if cls.is_the_only_available():
            return True

        configured_framework = cls.settings(
            'test_framework', framework=False, fallback=False
        )

        return (
            cls.is_configurable_fallback(file)
            if configured_framework is None
            else configured_framework == cls.framework
        )

    @classmethod
    def is_configurable_fallback(cls, _):
        return False
