from AnyTest.tests import SublimeProjectTestCase


class MavenJUnit3TestCase(SublimeProjectTestCase):
    folder = ('junit', 'maven', 'junit3')

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


class MavenJUnit3MultiModuleTestCase(SublimeProjectTestCase):
    folder = ('junit', 'maven', 'junit3_multi_module')

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


class MavenJUnit5TestCase(SublimeProjectTestCase):
    folder = ('junit', 'maven', 'junit5')

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


class MavenJUnit5MvnwTestCase(SublimeProjectTestCase):
    folder = ('junit', 'maven', 'junit5_mvnw')

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


class MavenJUnit5MultiModuleTestCase(SublimeProjectTestCase):
    folder = ('junit', 'maven', 'junit5_multi_module')

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


class GradleJUnit3PlainTestCase(SublimeProjectTestCase):
    folder = ('junit', 'gradle', 'junit3_plain')

    def test_line(self):
        yield from self._testFile('MathTest.java', 37)
        self.assertLastCommand('gradle test --tests MathTest.testFailedAdd')

    def test_file(self):
        yield from self._testFile('TestMath.java')
        self.assertLastCommand('gradle test --tests TestMath')

        yield from self._testFile('MathTest.java')
        self.assertLastCommand('gradle test --tests MathTest')

        yield from self._testFile('MathTests.java')
        self.assertLastCommand('gradle test --tests MathTests')

        yield from self._testFile('MathTestCase.java')
        self.assertLastCommand('gradle test --tests MathTestCase')

    def test_suite(self):
        yield from self._testSuite('MathTest.java')
        self.assertLastCommand('gradle test')


class GradleJUnit3SingleModuleTestCase(SublimeProjectTestCase):
    folder = ('junit', 'gradle', 'junit3_single_module')

    def test_line(self):
        yield from self._testFile(('src', 'test', 'java', 'MathTest.java'), 37)
        self.assertLastCommand('gradle test --tests MathTest.testFailedAdd')

    def test_file(self):
        yield from self._testFile(('src', 'test', 'java', 'TestMath.java'))
        self.assertLastCommand('gradle test --tests TestMath')

        yield from self._testFile(('src', 'test', 'java', 'MathTest.java'))
        self.assertLastCommand('gradle test --tests MathTest')

        yield from self._testFile(('src', 'test', 'java', 'MathTests.java'))
        self.assertLastCommand('gradle test --tests MathTests')

        yield from self._testFile(('src', 'test', 'java', 'MathTestCase.java'))
        self.assertLastCommand('gradle test --tests MathTestCase')

    def test_suite(self):
        yield from self._testSuite(('src', 'test', 'java', 'MathTest.java'))
        self.assertLastCommand('gradle test')


class GradleJUnit3MultiModuleTestCase(SublimeProjectTestCase):
    folder = ('junit', 'gradle', 'junit3_multi_module')

    def test_line(self):
        yield from self._testFile(
            ('sample_module', 'src', 'test', 'java', 'MathTest.java'), 37
        )
        self.assertLastCommand(
            'gradle test -p sample_module --tests MathTest.testFailedAdd'
        )

    def test_file(self):
        yield from self._testFile(
            ('sample_module', 'src', 'test', 'java', 'TestMath.java')
        )
        self.assertLastCommand('gradle test -p sample_module --tests TestMath')

        yield from self._testFile(
            ('sample_module', 'src', 'test', 'java', 'MathTest.java')
        )
        self.assertLastCommand('gradle test -p sample_module --tests MathTest')

        yield from self._testFile(
            ('sample_module', 'src', 'test', 'java', 'MathTests.java')
        )
        self.assertLastCommand('gradle test -p sample_module --tests MathTests')

        yield from self._testFile(
            ('sample_module', 'src', 'test', 'java', 'MathTestCase.java')
        )
        self.assertLastCommand('gradle test -p sample_module --tests MathTestCase')

    def test_suite(self):
        yield from self._testSuite(
            ('sample_module', 'src', 'test', 'java', 'MathTest.java')
        )
        self.assertLastCommand('gradle test -p sample_module')


class GradleJUnit3MultiModuleDeepTestCase(SublimeProjectTestCase):
    folder = ('junit', 'gradle', 'junit3_multi_module_deep')

    def test_file(self):
        yield from self._testFile(
            ('hello', 'world', 'src', 'test', 'java', 'MessageServiceTest.java')
        )
        self.assertLastCommand(
            'gradle test -p ', ('hello', 'world'), ' --tests MessageServiceTest'
        )


class GradleJUnit5PlainTestCase(SublimeProjectTestCase):
    folder = ('junit', 'gradle', 'junit5_plain')

    def test_line_nested(self):
        yield from self._testFile('MathJunit5Test.java', 57)
        self.assertLastCommand(
            'gradle test --tests MathJunit5Test\\$NestedClass.testNested'
        )

        self._testLine(64)
        self.assertLastCommand(
            'gradle test --tests MathJunit5Test\\$NestedClass.testNested2'
        )

    def test_line_leveled_nested(self):
        yield from self._testFile('MathJunit5Test.java', 74)
        self.assertLastCommand(
            'gradle test --tests MathJunit5Test\\$NestedClass\\$NestedNestedClass.testNestedNested'
        )

    def test_line_nested_parameterized_test_and_source_methods(self):
        yield from self._testFile('MathJunit5Test.java', 91)
        self.assertLastCommand(
            'gradle test --tests MathJunit5Test\\$NestedParameterizedTestClass.testWithParams'
        )

    def test_line_nested_parameterized_test_combined(self):
        yield from self._testFile('MathJunit5Test.java', 91)
        self.assertLastCommand(
            'gradle test --tests MathJunit5Test\\$NestedParameterizedTestClass.testWithParams'
        )
