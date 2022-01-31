class IsConfigurableMixin:
    @classmethod
    def is_suitable_for(cls, file):
        if not super().is_suitable_for(file):
            return False

        configured_framework = cls.settings(
            'test_framework', framework=False, fallback=False
        )

        if configured_framework is None:
            return cls.is_configurable_fallback(file)
        else:
            return configured_framework == cls.framework

    @classmethod
    def is_configurable_fallback(cls, _):
        return False
