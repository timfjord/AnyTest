from .. import javascript


class TestFramework(javascript.TestFramework):
    framework = 'jest'
    pattern = r'(__tests__/.*|(spec|test))\.(js|jsx|coffee|ts|tsx)$'
