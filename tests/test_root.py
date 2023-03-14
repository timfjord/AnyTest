# isort:skip_file

import os
import tempfile
import unittest

import sublime

from AnyTest.plugin import errors
from AnyTest.plugin.root import File, Glob, RelativePath, Root
from AnyTest.tests import FIXTURES_PATH

IS_WINDOWS = sublime.platform() == "windows"


DIR = "C:\\st" if IS_WINDOWS else "~"


def path(*parts):
    return os.path.join(DIR, *parts)


class RootTestCase(unittest.TestCase):
    def test_find_handles_invalid_files(self):
        with self.assertRaises(errors.InvalidContext):
            Root.find([], None)

    def test_find_handles_empty_folders(self):
        with self.assertRaises(errors.InvalidContext):
            Root.find([], path("code", "another_project", "file.py"))

    def test_find_handles_files_outside_the_folder(self):
        with self.assertRaises(errors.InvalidContext):
            Root.find(
                [path("code", "project")], path("code", "another_project", "file.py")
            )

    def test_find_returns_the_root_and_the_file(self):
        root_path = path("code", "project")
        file_path = path("code", "project", "file.py")
        root, file = Root.find([root_path], file_path)

        self.assertIsInstance(root, Root)
        self.assertEqual(root.path, root_path)
        self.assertIsInstance(file, File)
        self.assertEqual(file.path, file_path)

    def test_find_tests_the_longest_folders_first(self):
        root_path1 = path("code", "project")
        root_path2 = path("code", "project", "folder")
        file_path = path("code", "project", "folder", "file.py")
        root, file = Root.find([root_path1, root_path2], file_path)

        self.assertEqual(root.path, root_path2)
        self.assertEqual(file.path, file_path)

    def test_find_supports_subprojects(self):
        root_path = path("code", "project")
        subproject1 = os.path.join("folder", "subfolder1")
        subproject2 = ("folder", "subfolder2")
        file_path = path("code", "project", "folder", "subfolder2", "file.py")
        root, file = Root.find([root_path], file_path, [subproject1, subproject2])

        self.assertEqual(
            root.path, os.path.join(root_path, subproject2[0], subproject2[1])
        )
        self.assertEqual(file.path, file_path)

    def test_find_projects_and_subprojects_longest_folder_first(self):
        root_path1 = path("code", "project")
        root_path2 = path("code", "project", "folder", "subfolder1", "subfolder1_1")
        subproject1 = os.path.join("folder", "subfolder1")
        subproject2 = ("folder", "subfolder2")
        file_path = path(
            "code", "project", "folder", "subfolder1", "subfolder1_1", "file.py"
        )
        root, file = Root.find(
            [root_path1, root_path2], file_path, [subproject1, subproject2]
        )

        self.assertEqual(root.path, root_path2)
        self.assertEqual(file.path, file_path)

    def test_name(self):
        root_path = path("code", "project")
        root = Root(root_path)

        self.assertEqual(root.name(), "project")

    def test_join_joins_files_to_the_root(self):
        root_path = path("code", "project")
        root = Root(root_path)

        self.assertEqual(
            root.join("folder", "file.py"), os.path.join(root_path, "folder", "file.py")
        )

    def test_relpath_returns_relative_path(self):
        root = Root(path("code", "project"))

        self.assertEqual(root.relpath(path("code", "project", "file.py")), "file.py")

    def test_file_instantiates_a_file_instance(self):
        file = Root(path("code", "project")).file("folder", "file.py")

        self.assertIsInstance(file, File)
        self.assertEqual(file.path, path("code", "project", "folder", "file.py"))

    def test_parent(self):
        root = Root(path("code", "project"))
        parent = root.parent()

        self.assertIsInstance(parent, Root)
        self.assertEqual(parent.path, path("code"))

    def test_glob(self):
        root = Root(path("code"))
        glob = root.glob("cucumber", "**", "*.rb")

        self.assertIsInstance(glob, Glob)
        self.assertEqual(glob.pattern, path("code", "cucumber", "**", "*.rb"))


def build_temp_files(tmpfile):
    existing_file = os.path.basename(tmpfile.name)
    root = Root(os.path.dirname(tmpfile.name))
    existing_dir = os.path.basename(root.path)
    subfolder = Root(os.path.dirname(root.path))

    return existing_file, root, existing_dir, subfolder


class RelativePathTestCase(unittest.TestCase):
    def test_realative_path_calculation_on_init(self):
        root = Root(path("code", "project"))
        relative_path = RelativePath(root, "folder", "file.py")

        self.assertEqual(relative_path.relpath, os.path.join("folder", "file.py"))
        self.assertEqual(
            relative_path.path, path("code", "project", "folder", "file.py")
        )

    def test_exists_checks_if_path_exists(self):
        with tempfile.NamedTemporaryFile() as tmpfile:
            existing_file, root, existing_dir, subfolder = build_temp_files(tmpfile)

            self.assertTrue(RelativePath(root, existing_file).exists())
            self.assertFalse(RelativePath(root, "uNkn0wn.py").exists())
            self.assertTrue(RelativePath(subfolder, existing_dir).exists())

    def test_dir(self):
        root = Root(path("code", "project"))
        relative_path = RelativePath(root, "folder", "file.py")
        dir = relative_path.dir()

        self.assertIsInstance(dir, Root)
        self.assertEqual(dir.path, path("code", "project", "folder"))

    def test_dirname(self):
        root = Root(path("code", "project"))
        relative_path = RelativePath(root, "folder", "file.py")

        self.assertEqual(relative_path.dirname(), "folder")

    def test_parent(self):
        root = Root(path("code", "project"))
        relative_path = RelativePath(root, "folder", "file.py")
        parent = relative_path.parent()

        self.assertIsInstance(parent, Root)
        self.assertEqual(parent.path, path("code", "project"))

    def test_name(self):
        root = Root(path("code", "project"))
        relative_path = RelativePath(root, "folder", "file.py")

        self.assertEqual(relative_path.name(), "file")

    def test_is_in_root(self):
        root = Root(path("code", "project"))
        relative_path1 = RelativePath(root, "file.py")
        relative_path2 = RelativePath(root, "folder", "file.py")

        self.assertTrue(relative_path1.is_in_root())
        self.assertFalse(relative_path2.is_in_root())


class FileTestCase(unittest.TestCase):
    def test_exists_checks_if_file_exists(self):
        with tempfile.NamedTemporaryFile() as tmpfile:
            existing_file, root, existing_dir, subfolder = build_temp_files(tmpfile)

            self.assertTrue(File(root, existing_file).exists())
            self.assertFalse(File(root, "uNkn0wn.py").exists())
            self.assertFalse(File(subfolder, existing_dir).exists())

    @unittest.skipIf(IS_WINDOWS, "[Errno 13] Permission denied")
    def test_lines(self):
        with tempfile.NamedTemporaryFile("w") as tmpfile:
            tmpfile.write("line1\nline2\nline3")
            tmpfile.seek(0)
            file_name = os.path.basename(tmpfile.name)
            root = Root(os.path.dirname(tmpfile.name))
            file = File(root, file_name)
            lines = [line for line in file.lines()]

            self.assertEqual(lines, ["line1", "line2", "line3"])

    @unittest.skipIf(IS_WINDOWS, "[Errno 13] Permission denied")
    def test_contains_line(self):
        with tempfile.NamedTemporaryFile("w") as tmpfile:
            tmpfile.write("some content goes here")
            tmpfile.seek(0)
            file_name = os.path.basename(tmpfile.name)
            root = Root(os.path.dirname(tmpfile.name))
            file = File(root, file_name)

            self.assertTrue(file.contains_line("content"))
            self.assertFalse(file.contains_line("uNkn0wn"))

    def test_dir_relpath(self):
        root = Root(path("code", "project"))
        relative_path = File(root, "folder1", "folder2", "file.py")

        self.assertEqual(
            relative_path.dir_relpath(), os.path.join("folder1", "folder2")
        )


class GlobTestCase(unittest.TestCase):
    def test_iter(self):
        root = Root(FIXTURES_PATH)
        glob = Glob(root, "cucumber", "**", "*.rb")
        iter = glob.__iter__()

        self.assertIsInstance(iter, map)
        self.assertEqual(list(iter), [root.join("cucumber", "features", "code.rb")])
        self.assertTrue(any(glob))
