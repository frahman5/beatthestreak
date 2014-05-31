import unittest

from datetime import date
from data import Data
from tests import setup, teardown, r2013
from utilities import Utilities

# @unittest.skip("Focus is not on Utilities right now")
class TestUtilities(unittest.TestCase):

    def setUp(self):
        setup()
        
    def tearDown(self):
        teardown()
    
    def test_convert_date(self):
        self.assertEqual(Utilities.convert_date(date(2012, 4, 15)),"20120415")

    def test_clean_retrosheet_files(self):
        r2013.download_and_unzip() # assume works

        Utilities.clean_retrosheet_files()
        # Is zipped folder clean?
        zippedFileFolder = Data.get_retrosheet_zipped_folder_path()
        os.chdir(zippedFileFolder)
        self.assertEqual(os.listdir(os.getcwd()),[])

        # is unzipped folder clean??
        unzippedFileFolder = Data.get_retrosheet_unzipped_folder_path()
        os.chdir(unzippedFileFolder)
        self.assertEqual(os.listdir(os.getcwd()), [])