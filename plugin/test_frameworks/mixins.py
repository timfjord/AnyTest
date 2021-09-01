class SuitableMixin:
    @classmethod
    def is_suitable_for(cls, file):
        if not super().is_suitable_for(file):
            return False

        return cls.settings(
            'framework', language=True
        ) == cls.framework or cls.is_suitable(file)

    @classmethod
    def is_suitable(cls, _):
        return False
