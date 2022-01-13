import os
import tempfile
import unittest

import sublime

from AnyTest.plugin import errors
from AnyTest.plugin.root import File, RelativePath, Root


IS_WINDOWS = sublime.platform() == 'windows'


DIR = 'C:\\st' if IS_WINDOWS else '~'


def path(*parts):
    return os.path.join(DIR, *parts)


class RootTestCase(unittest.TestCase):
    def test_find_handles_invalid_files(self):
        with self.assertRaises(errors.InvalidContext):
            Root.find([], None)

    def test_find_handles_empty_folders(self):
        with self.assertRaises(errors.InvalidContext):
            Root.find([], path('code', 'another_project', 'file.py'))

    def test_find_handles_files_outside_the_folder(self):
        with self.assertRaises(errors.InvalidContext):
            Root.find(
                [path('code', 'project')], path('code', 'another_project', 'file.py')
            )

    def test_find_returns_the_root_and_the_file(self):
        root_path = path('code', 'project')
        file_path = path('code', 'project', 'file.py')
        root, file = Root.find([root_path], file_path)

        self.assertIsInstance(root, Root)
        self.assertEqual(root.path, root_path)
        self.assertIsInstance(file, File)
        self.assertEqual(file.path, file_path)

    def test_find_tests_the_longest_folders_first(self):
        root_path1 = path('code', 'project')
        root_path2 = path('code', 'project', 'folder')
        file_path = path('code', 'project', 'folder', 'file.py')
        root, file = Root.find([root_path1, root_path2], file_path)

        self.assertEqual(root.path, root_path2)
        self.assertEqual(file.path, file_path)

    def test_join_joins_files_to_the_root(self):
        root_path = path('code', 'project')
        root = Root(root_path)

        self.assertEqual(
            root.join('folder', 'file.py'), os.path.join(root_path, 'folder', 'file.py')
        )

    def test_relpath_returns_relative_path(self):
        root = Root(path('code', 'project'))

        self.assertEqual(root.relpath(path('code', 'project', 'file.py')), 'file.py')

    def test_file_instantiates_a_file_instance(self):
        file = Root(path('code', 'project')).file('folder', 'file.py')

        self.assertIsInstance(file, File)
        self.assertEqual(file.path, path('code', 'project', 'folder', 'file.py'))


class RelativePathTestCase(unittest.TestCase):
    def test_realative_path_calculation_on_init(self):
        root = Root(path('code', 'project'))
        relative_path = RelativePath(root, 'folder', 'file.py')

        self.assertEqual(relative_path.relpath, os.path.join('folder', 'file.py'))
        self.assertEqual(
            relative_path.path, path('code', 'project', 'folder', 'file.py')
        )

    def test_exists_checks_if_path_exists(self):
        with tempfile.NamedTemporaryFile() as tmpfile:
            existing_file = os.path.basename(tmpfile.name)
            root = Root(os.path.dirname(tmpfile.name))
            existing_dir = os.path.basename(root.path)
            subfolder = Root(os.path.dirname(root.path))

            self.assertTrue(RelativePath(root, existing_file).exists())
            self.assertFalse(RelativePath(root, 'uNkn0wn.py').exists())
            self.assertTrue(RelativePath(subfolder, existing_dir).exists())


class FileTestCase(unittest.TestCase):
    def test_exists_checks_if_file_exists(self):
        with tempfile.NamedTemporaryFile() as tmpfile:
            existing_file = os.path.basename(tmpfile.name)
            root = Root(os.path.dirname(tmpfile.name))
            existing_dir = os.path.basename(root.path)
            subfolder = Root(os.path.dirname(root.path))

            self.assertTrue(File(root, existing_file).exists())
            self.assertFalse(File(root, 'uNkn0wn.py').exists())
            self.assertFalse(File(subfolder, existing_dir).exists())

    @unittest.skipIf(IS_WINDOWS, '[Errno 13] Permission denied')
    def test_contains(self):
        with tempfile.NamedTemporaryFile('w') as tmpfile:
            tmpfile.write('some content goes here')
            tmpfile.seek(0)
            file_name = os.path.basename(tmpfile.name)
            root = Root(os.path.dirname(tmpfile.name))
            file = File(root, file_name)

            self.assertTrue(file.contains('content'))
            self.assertFalse(file.contains('uNkn0wn'))
