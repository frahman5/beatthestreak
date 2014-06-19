import unittest
import os

from datetime import date

from beatthestreak.filepath import Filepath
from beatthestreak.tests import setup, teardown, r2013
from beatthestreak.utilities import Utilities

class TestUtilities(unittest.TestCase):

    def setUp(self):
        setup()
        
    def tearDown(self):
        teardown()
    
    def test_convert_date(self):
        self.assertEqual(Utilities.convert_date(date(2012, 4, 15)),"20120415")

    @skip("Don't want to delete retrosheet files!")
    def test_clean_retrosheet_files(self):
        r2013.download_and_unzip() # assume works

        Utilities.clean_retrosheet_files()
        # Is zipped folder clean?
        zippedFileFolder = Filepath.get_retrosheet_folder(folder='zipped')
        os.chdir(zippedFileFolder)
        self.assertEqual(os.listdir(os.getcwd()),[])

        # is unzipped folder clean??
        unzippedFileFolder = Filepath.get_retrosheet_folder(folder='unzipped')
        os.chdir(unzippedFileFolder)
        self.assertEqual(os.listdir(os.getcwd()), [])

    def test_ensure_gamelog_files_exist(self):
        # gamelog files should be nonexistant before hand
        self.assertFalse(os.path.isfile(Filepath.get_retrosheet_file(
            folder='unzipped', fileF='gamelog', year=2010)))

        Utilities.ensure_gamelog_files_exist(2010)

        # gamelog files exist after function call
        self.assertTrue(os.path.isfile(Filepath.get_retrosheet_file(
            folder='unzipped', fileF='gamelog', year=2010)))

    def test_ensure_boxscore_files_exist(self):
        # boxscore files should be nonexistant before hand
        self.assertFalse(os.path.isfile(Filepath.get_retrosheet_file(
            folder='unzipped', fileF='boxscore', year=2008, team='HOU')))

        Utilities.ensure_boxscore_files_exist(2008, 'HOU')

        # boxscore files exist after function call
        self.assertTrue(os.path.isfile(Filepath.get_retrosheet_file(
            folder='unzipped', fileF='boxscore', year=2008, team='HOU')))