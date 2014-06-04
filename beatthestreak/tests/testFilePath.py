import unittest

from beatthestreak.filepath import FilePath
from beatthestreak.tests import setup, teardown

class TestFilePath(unittest.TestCase):
    """
    As these tests use filepaths native to the development
    machine, they only work on the development machine
    """

    def setUp(self):
        self.rootDir = '/Users/faiyamrahman/programming/Python/beatthestreak' + \
        '/beatthestreak'
        setup()
        
    def tearDown(self):
        teardown()

    def test_get_root(self):
        self.assertEqual(FilePath.get_root(),self.rootDir)

    def test_get_retrosheet_folder(self):
        self.assertEqual(FilePath.get_retrosheet_folder(folder='base'), 
            self.rootDir + '/datasets/retrosheet')
        self.assertEqual(FilePath.get_retrosheet_folder(folder='zipped'), 
            self.rootDir + '/datasets/retrosheet/zipped')
        self.assertEqual(FilePath.get_retrosheet_folder(folder='unzipped'), 
            self.rootDir + '/datasets/retrosheet/unzipped')
        self.assertEqual(FilePath.get_retrosheet_folder(folder='persistent'), 
            self.rootDir + '/datasets/retrosheet/persistent')
