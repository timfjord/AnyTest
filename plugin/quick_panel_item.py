try:
    from sublime import QuickPanelItem
except ImportError:

    class QuickPanelItem(list):
        def __init__(self, trigger, details, annotation, _=None):
            self.trigger = trigger
            self.details = details
            self.annotation = annotation

            super().__init__(
                filter(None, [self.trigger, self.details, self.annotation])
            )


__all__ = ["QuickPanelItem"]
