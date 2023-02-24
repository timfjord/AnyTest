from AnyTest.tests import SublimeProjectTestCase


class MaventestJunit3TestCase(SublimeProjectTestCase):
    folder = ('maventest', 'junit3')

    def test_line(self):
        yield from self._testFile(
            ('src', 'test', 'java', 'org', 'anytest', 'math', 'MathTest.java'), 37
        )

        self.assertLastCommand(
            'mvn test -Dtest=org.anytest.math.MathTest#testFailedAdd'
        )

    def test_file(self):
        yield from self._testFile(
            ('src', 'test', 'java', 'org', 'anytest', 'math', 'TestMath.java')
        )
        self.assertLastCommand('mvn test -Dtest=org.anytest.math.TestMath\\*')

        yield from self._testFile(
            ('src', 'test', 'java', 'org', 'anytest', 'math', 'MathTest.java')
        )
        self.assertLastCommand('mvn test -Dtest=org.anytest.math.MathTest\\*')

        yield from self._testFile(
            ('src', 'test', 'java', 'org', 'anytest', 'math', 'MathTests.java')
        )
        self.assertLastCommand('mvn test -Dtest=org.anytest.math.MathTests\\*')

        yield from self._testFile(
            ('src', 'test', 'java', 'org', 'anytest', 'math', 'MathTestCase.java')
        )
        self.assertLastCommand('mvn test -Dtest=org.anytest.math.MathTestCase\\*')

    def test_suite(self):
        yield from self._testSuite(
            ('src', 'test', 'java', 'org', 'anytest', 'math', 'MathTest.java')
        )
        self.assertLastCommand('mvn test')


class MaventestJunit3MultimoduleTestCase(SublimeProjectTestCase):
    folder = ('maventest', 'junit3_multimodule')

    def test_line(self):
        yield from self._testFile(
            (
                'sample_module',
                'src',
                'test',
                'java',
                'org',
                'anytest',
                'math',
                'MathTest.java',
            ),
            37,
        )

        self.assertLastCommand(
            'mvn test -pl sample_module -Dtest=org.anytest.math.MathTest#testFailedAdd'
        )

    def test_file(self):
        yield from self._testFile(
            (
                'sample_module',
                'src',
                'test',
                'java',
                'org',
                'anytest',
                'math',
                'TestMath.java',
            )
        )
        self.assertLastCommand(
            'mvn test -pl sample_module -Dtest=org.anytest.math.TestMath\\*'
        )

        yield from self._testFile(
            (
                'sample_module',
                'src',
                'test',
                'java',
                'org',
                'anytest',
                'math',
                'MathTest.java',
            )
        )
        self.assertLastCommand(
            'mvn test -pl sample_module -Dtest=org.anytest.math.MathTest\\*'
        )

        yield from self._testFile(
            (
                'sample_module',
                'src',
                'test',
                'java',
                'org',
                'anytest',
                'math',
                'MathTests.java',
            )
        )
        self.assertLastCommand(
            'mvn test -pl sample_module -Dtest=org.anytest.math.MathTests\\*'
        )

        yield from self._testFile(
            (
                'sample_module',
                'src',
                'test',
                'java',
                'org',
                'anytest',
                'math',
                'MathTestCase.java',
            )
        )
        self.assertLastCommand(
            'mvn test -pl sample_module -Dtest=org.anytest.math.MathTestCase\\*'
        )

    def test_suite(self):
        yield from self._testSuite(
            (
                'sample_module',
                'src',
                'test',
                'java',
                'org',
                'anytest',
                'math',
                'MathTest.java',
            )
        )
        self.assertLastCommand('mvn test -pl sample_module')


class MaventestJunit5TestCase(SublimeProjectTestCase):
    folder = ('maventest', 'junit5')

    def test_line(self):
        yield from self._testFile(
            ('src', 'test', 'java', 'org', 'anytest', 'TestApp.java'), 12
        )
        self.assertLastCommand(
            'mvn test -Dtest=org.anytest.TestApp#test_testdecorator_void'
        )

        self._testLine(17)
        self.assertLastCommand(
            'mvn test -Dtest=org.anytest.TestApp#test_testdecorator_public_void'
        )

        self._testLine(22)
        self.assertLastCommand('mvn test -Dtest=org.anytest.TestApp#test_void')

        self._testLine(30)
        self.assertLastCommand('mvn test -Dtest=org.anytest.TestApp#test_public_void')

        self._testLine(39)
        self.assertLastCommand(
            'mvn test -Dtest=org.anytest.TestApp\\$Test_NestedTestClass#test_nested_test'
        )

    def test_file(self):
        yield from self._testFile(
            ('src', 'test', 'java', 'org', 'anytest', 'TestApp.java')
        )
        self.assertLastCommand('mvn test -Dtest=org.anytest.TestApp\\*')


class MaventestJunit5MvnwTestCase(SublimeProjectTestCase):
    folder = ('maventest', 'junit5_mvnw')

    def test_line(self):
        yield from self._testFile(
            ('src', 'test', 'java', 'org', 'anytest', 'TestApp.java'), 12
        )
        self.assertLastCommand(
            './mvnw test -Dtest=org.anytest.TestApp#test_testdecorator_void'
        )

        self._testLine(17)
        self.assertLastCommand(
            './mvnw test -Dtest=org.anytest.TestApp#test_testdecorator_public_void'
        )

        self._testLine(22)
        self.assertLastCommand('./mvnw test -Dtest=org.anytest.TestApp#test_void')

        self._testLine(30)
        self.assertLastCommand(
            './mvnw test -Dtest=org.anytest.TestApp#test_public_void'
        )

        self._testLine(39)
        self.assertLastCommand(
            './mvnw test -Dtest=org.anytest.TestApp\\$Test_NestedTestClass#test_nested_test'
        )

    def test_file(self):
        yield from self._testFile(
            ('src', 'test', 'java', 'org', 'anytest', 'TestApp.java')
        )
        self.assertLastCommand('./mvnw test -Dtest=org.anytest.TestApp\\*')


class MaventestJunit5MultimoduleTestCase(SublimeProjectTestCase):
    folder = ('maventest', 'junit5_multimodule')

    def test_line(self):
        yield from self._testFile(
            ('sample_module', 'src', 'test', 'java', 'org', 'anytest', 'TestApp.java'),
            12,
        )
        self.assertLastCommand(
            'mvn test -pl sample_module -Dtest=org.anytest.TestApp#test_testdecorator_void'
        )

        self._testLine(17)
        self.assertLastCommand(
            'mvn test -pl sample_module -Dtest=org.anytest.TestApp#test_testdecorator_public_void'
        )

        self._testLine(22)
        self.assertLastCommand(
            'mvn test -pl sample_module -Dtest=org.anytest.TestApp#test_void'
        )

        self._testLine(30)
        self.assertLastCommand(
            'mvn test -pl sample_module -Dtest=org.anytest.TestApp#test_public_void'
        )

        self._testLine(39)
        self.assertLastCommand(
            'mvn test -pl sample_module '
            '-Dtest=org.anytest.TestApp\\$Test_NestedTestClass#test_nested_test'
        )

    def test_file(self):
        yield from self._testFile(
            ('sample_module', 'src', 'test', 'java', 'org', 'anytest', 'TestApp.java')
        )
        self.assertLastCommand(
            'mvn test -pl sample_module -Dtest=org.anytest.TestApp\\*'
        )
