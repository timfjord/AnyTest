class IsConfigurableMixin:
    @classmethod
    def is_suitable_for(cls, file):
        if not super().is_suitable_for(file):
            return False

        return cls.settings(
            'test_framework', framework=False, fallback=False
        ) == cls.framework or cls.is_configurable_fallback(file)

    @classmethod
    def is_configurable_fallback(cls, _):
        return False
