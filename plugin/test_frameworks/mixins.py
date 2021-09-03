class IsAppropriateMixin:
    @classmethod
    def is_suitable_for(cls, file):
        if not super().is_suitable_for(file):
            return False

        return cls.settings(
            'framework', framework=False, fallback=False
        ) == cls.framework or cls.is_appropriate_for(file)

    @classmethod
    def is_appropriate_for(cls, _):
        return False
