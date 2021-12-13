import os
import tempfile
from unittest import TestCase

from AnyTest.plugin import errors
from AnyTest.plugin.root import File, RelativePath, Root


class RootTestCase(TestCase):
    def test_find_handles_invalid_files(self):
        with self.assertRaises(errors.InvalidContext):
            Root.find([], None)

    def test_find_handles_empty_folders(self):
        with self.assertRaises(errors.InvalidContext):
            Root.find([], '~/code/another_project/file.py')

    def test_find_handles_files_outside_the_folder(self):
        with self.assertRaises(errors.InvalidContext):
            Root.find(['~/code/project'], '~/code/another_project/file.py')

    def test_find_returns_the_root_and_the_file(self):
        root, file = Root.find(['~/code/project'], '~/code/project/file.py')

        self.assertIsInstance(root, Root)
        self.assertEqual(root.path, '~/code/project')
        self.assertIsInstance(file, File)
        self.assertEqual(file.path, '~/code/project/file.py')

    def test_find_tests_the_longest_folders_first(self):
        root, file = Root.find(
            ['~/code/project', '~/code/project/folder'], '~/code/project/folder/file.py'
        )

        self.assertEqual(root.path, '~/code/project/folder')
        self.assertEqual(file.path, '~/code/project/folder/file.py')

    def test_join_joins_files_to_the_root(self):
        root = Root('~/code/project')

        self.assertEqual(
            root.join('folder', 'file.py'), '~/code/project/folder/file.py'
        )

    def test_relpath_returns_relative_path(self):
        root = Root('~/code/project')

        self.assertEqual(root.relpath('~/code/project/file.py'), 'file.py')

    def test_file_instantiates_a_file_instance(self):
        file = Root('~/code/project').file('folder', 'file.py')

        self.assertIsInstance(file, File)
        self.assertEqual(file.path, '~/code/project/folder/file.py')


class RelativePathTestCase(TestCase):
    def test_realative_path_calculation_on_init(self):
        root = Root('~/code/project')
        relative_path = RelativePath(root, 'folder', 'file.py')

        self.assertEqual(relative_path.relpath, 'folder/file.py')
        self.assertEqual(relative_path.path, '~/code/project/folder/file.py')

    def test_exists_checks_if_path_exists(self):
        with tempfile.NamedTemporaryFile() as tmpfile:
            existing_file = os.path.basename(tmpfile.name)
            root = Root(os.path.dirname(tmpfile.name))
            existing_dir = os.path.basename(root.path)
            subfolder = Root(os.path.dirname(root.path))

            self.assertTrue(RelativePath(root, existing_file).exists())
            self.assertFalse(RelativePath(root, 'uNkn0wn.py').exists())
            self.assertTrue(RelativePath(subfolder, existing_dir).exists())


class FileTestCase(TestCase):
    def test_exists_checks_if_file_exists(self):
        with tempfile.NamedTemporaryFile() as tmpfile:
            existing_file = os.path.basename(tmpfile.name)
            root = Root(os.path.dirname(tmpfile.name))
            existing_dir = os.path.basename(root.path)
            subfolder = Root(os.path.dirname(root.path))

            self.assertTrue(File(root, existing_file).exists())
            self.assertFalse(File(root, 'uNkn0wn.py').exists())
            self.assertFalse(File(subfolder, existing_dir).exists())

    def test_contains(self):
        with tempfile.NamedTemporaryFile('w') as tmpfile:
            tmpfile.write('some content goes here')
            tmpfile.seek(0)
            file_name = os.path.basename(tmpfile.name)
            root = Root(os.path.dirname(tmpfile.name))
            file = File(root, file_name)

            self.assertTrue(file.contains('content'))
            self.assertFalse(file.contains('uNkn0wn'))
