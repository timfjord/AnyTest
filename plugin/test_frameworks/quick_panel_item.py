import sublime

if hasattr(sublime, 'QuickPanelItem'):

    class Base(sublime.QuickPanelItem):
        def __init__(self, language, framework):
            super().__init__(framework, '', language)

        @property
        def language(self):
            return self.annotation

        @property
        def framework(self):
            return self.trigger

else:

    class Base(list):
        def __init__(self, language, framework):
            super().__init__([framework, language])

        @property
        def language(self):
            return self[1]

        @property
        def framework(self):
            return self[0]


class QuickPanelItem(Base):
    def signature(self):
        return (self.language, self.framework)
