import unittest
import os
from g import *
from data import Data
import shutil
class TestRetrosheet(unittest.TestCase):

    def setUp(self):
        # Clean out zipped file folder of everything
        zippedFileFolder = Data.rootDir + Data.defaultDestZippedSuffix
        os.chdir(zippedFileFolder)
        for file in os.listdir(os.getcwd()): os.remove(file)

    def test_download(self):
        r2013.download()
        self.assertTrue(os.path.isfile(r2013.get_event_file_zipped()))

    def test_unzip(self):
        r2013.download() # assume works
        r2013.unzip()
        self.assertTrue(os.path.isfile(r2013.get_event_file_unzipped() + \
                                           "/2013ANA.EVA"))
        self.assertTrue(os.path.isfile(r2013.get_event_file_unzipped() + \
                                           "/2013OAK.EVA"))

    def test_gen_team_abbrevs(self):
        r2013.download() # assume works
        r2013.unzip() # assume works
        self.assertEqual(r2013.gen_team_abbrevs(),teamAbbrevs2013)

    def test_gen_boxscores(self):
        r2013.download() # assume works
        r2013.unzip() # assume works
        r2013.gen_boxscores()
        for path in boxscores2013:
            self.assertTrue(os.path.isfile(r2013.get_dest_unzipped() + \
                              "/events2013/" + path))

    # def test_clean_used_files(self):
    #     # Are the files there before we begin?
    #     for path in eventfiles2013:
    #         self.assertTrue(os.path.isfile(r2013.get_dest_unzipped() + \
    #                                       "/events2013/" + path))
    #     r2013.clean_used_files()
    #     for path in eventfiles2013:
    #         self.assertFalse(os.path.isfile(r2013.get_dest_unzipped() + \
    #                                         "/events2013/" + path))
    def tearDown(self):
        # Clean out zipped file folder afterwards
        zippedFileFolder = Data.rootDir + Data.defaultDestZippedSuffix
        os.chdir(zippedFileFolder)
        for file in os.listdir(os.getcwd()): 
          if os.path.isdir(file): 
            shutil.rmtree(file)
          else: 
            os.remove(file) 

        # Clean out unzipped file folder as well ##NEED TO LET IT HANDLE ALL FOLDERS
        unzippedFileFolder = Data.rootDir + Data.defaultDestUnzippedSuffix
        os.chdir(unzippedFileFolder)
        for file in os.listdir(os.getcwd()): 
          if os.path.isdir(file): 
            shutil.rmtree(file)
          else: 
            os.remove(file) 