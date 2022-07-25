from AnyTest.tests import SublimeProjectTestCase


class CargotestTestCase(SublimeProjectTestCase):
    folder = ('cargotest', 'crate')

    def test_line_on_lib(self):
        yield from self._testFile(('src', 'lib.rs'), 5)
        self.assertLastCommand('cargo test tests::first_test -- --exact')

        self._testLine(13)
        self.assertLastCommand('cargo test tests::third_test -- --exact')

        self._testLine(7)
        self.assertLastCommand('cargo test tests::second_test -- --exact')

    def test_line_on_modules_with_mod_as_test(self):
        yield from self._testFile(('src', 'somemod_test.rs'), 5)
        self.assertLastCommand('cargo test somemod_test::test::first_test -- --exact')

        self._testLine(13)
        self.assertLastCommand('cargo test somemod_test::test::third_test -- --exact')

        self._testLine(7)
        self.assertLastCommand('cargo test somemod_test::test::second_test -- --exact')

    def test_line_withou_mod(self):
        yield from self._testFile(('src', 'nomod.rs'), 2)
        self.assertLastCommand('cargo test nomod::first_test -- --exact')

        self._testLine(10)
        self.assertLastCommand('cargo test nomod::third_test -- --exact')

        self._testLine(6)
        self.assertLastCommand('cargo test nomod::second_test -- --exact')

    def test_line_on_modules(self):
        yield from self._testFile(('src', 'somemod.rs'), 5)
        self.assertLastCommand('cargo test somemod::tests::first_test -- --exact')

        self._testLine(13)
        self.assertLastCommand('cargo test somemod::tests::third_test -- --exact')

        self._testLine(7)
        self.assertLastCommand('cargo test somemod::tests::second_test -- --exact')

        yield from self._testFile(('src', 'nested', 'mod.rs'), 5)
        self.assertLastCommand('cargo test nested::tests::first_test -- --exact')

        self._testLine(13)
        self.assertLastCommand('cargo test nested::tests::third_test -- --exact')

        self._testLine(7)
        self.assertLastCommand('cargo test nested::tests::second_test -- --exact')

        yield from self._testFile(('src', 'too', 'nested.rs'), 5)
        self.assertLastCommand('cargo test too::nested::tests::first_test -- --exact')

        self._testLine(13)
        self.assertLastCommand('cargo test too::nested::tests::third_test -- --exact')

        self._testLine(7)
        self.assertLastCommand('cargo test too::nested::tests::second_test -- --exact')

    def test_line_async_tokio(self):
        yield from self._testFile(('src', 'lib.rs'), 15)
        self.assertLastCommand('cargo test tests::tokio_async_test -- --exact')

    def test_line_rstest(self):
        yield from self._testFile(('src', 'lib.rs'), 22)
        self.assertLastCommand('cargo test tests::rstest_test -- --exact')

    def test_line_async_actix_rt(self):
        yield from self._testFile(('src', 'lib.rs'), 26)
        self.assertLastCommand('cargo test tests::test_actix_rt -- --exact')

    def test_file(self):
        yield from self._testFile(('src', 'lib.rs'))
        self.assertLastCommand('cargo test')

        yield from self._testFile(('src', 'main.rs'))
        self.assertLastCommand('cargo test')

        yield from self._testFile(('src', 'somemod.rs'))
        self.assertLastCommand('cargo test somemod::')

        yield from self._testFile(('src', 'nested', 'mod.rs'))
        self.assertLastCommand('cargo test nested::')

        yield from self._testFile(('src', 'too', 'nested.rs'))
        self.assertLastCommand('cargo test too::nested::')

    def test_suite(self):
        yield from self._testSuite(('src', 'lib.rs'))
        self.assertLastCommand('cargo test')

        yield from self._testSuite(('src', 'somemod.rs'))
        self.assertLastCommand('cargo test')

        yield from self._testSuite(('src', 'nested', 'mod.rs'))
        self.assertLastCommand('cargo test')

        yield from self._testSuite(('src', 'too', 'nested.rs'))
        self.assertLastCommand('cargo test')


class CargotestWorkspaceTestCase(SublimeProjectTestCase):
    folder = 'cargotest'

    def test_file(self):
        yield from self._testFile(('crate', 'src', 'lib.rs'))
        self.assertLastCommand('cargo test --package crate')
