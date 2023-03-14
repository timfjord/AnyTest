from AnyTest.tests import SublimeProjectTestCase


class GinkgoTestCase(SublimeProjectTestCase):
    folder = "ginkgo"
    settings = {"go.test_framework": "ginkgo"}

    def test_line(self):
        yield from self._testFile("normal_test.go", 17)
        self.assertLastCommand("ginkgo --focus='should paginate the result' ./.")

        self._testLine(29)
        self.assertLastCommand("ginkgo --focus='user is not logged in' ./.")

        self._testLine(11)
        self.assertLastCommand("ginkgo --focus='when the request is authenticated' ./.")

        self._testLine(9)
        self.assertLastCommand("ginkgo --focus='posts API' ./.")

    def test_line_subdirectory(self):
        yield from self._testFile(("mypackage", "normal_test.go"), 17)
        self.assertLastCommand(
            "ginkgo --focus='should paginate the result' ./mypackage"
        )

    def test_line_no_nearest(self):
        yield from self._testFile(("mypackage", "normal_test.go"), 1)
        self.assertLastCommand(
            "ginkgo --focus-file=", ("mypackage", "normal_test.go"), " ./mypackage"
        )

    def test_file(self):
        yield from self._testFile("normal_test.go")
        self.assertLastCommand("ginkgo --focus-file=normal_test.go ./.")

    def test_file_subdirectory(self):
        yield from self._testFile(("mypackage", "normal_test.go"))
        self.assertLastCommand(
            "ginkgo --focus-file=", ("mypackage", "normal_test.go"), " ./mypackage"
        )

    def test_suite(self):
        yield from self._testSuite("normal_test.go")
        self.assertLastCommand("ginkgo ./.")

    def test_suite_package(self):
        yield from self._testSuite(("mypackage", "normal_test.go"))
        self.assertLastCommand("ginkgo ./mypackage")


class GinkgoAutodetectionTestCase(SublimeProjectTestCase):
    folder = "ginkgo"

    def test_line(self):
        yield from self._testFile("normal_test.go", 17)
        self.assertLastCommand("ginkgo --focus='should paginate the result' ./.")
