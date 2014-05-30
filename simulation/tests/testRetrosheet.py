import unittest
import os
from g import *
from data import Data
import shutil

# @unittest.skip("Focus is not in Retrosheet right now")
class TestRetrosheet(unittest.TestCase):

    def setUp(self):
        # Clean out zipped file folder of everything
        zippedFileFolder = Data.rootDir + Data.defaultDestZippedSuffix
        os.chdir(zippedFileFolder)
        for file in os.listdir(os.getcwd()): os.remove(file)

    def test_download(self):
        # test that we can download event files
        r2013.download(type='event')
        self.assertTrue(os.path.isfile(r2013.get_event_file_zipped()))

        # test that we can download gamelog files
        r2013.download(type='gamelog')
        self.assertTrue(os.path.isfile(r2013.get_gamelog_file_zipped()))

    def test_unzip(self):
        # test that we can unzip event files
        r2013.download(type='event') # assume works
        r2013.unzip(type='event')
        self.assertTrue(os.path.isfile(r2013.get_event_file_unzipped() + \
                                           "/2013ANA.EVA"))
        self.assertTrue(os.path.isfile(r2013.get_event_file_unzipped() + \
                                           "/2013OAK.EVA"))

        # test that we can unzip gamelog files
        r2013.download(type='gamelog') # assume works
        r2013.unzip(type='gamelog')
        self.assertTrue(os.path.isfile(r2013.get_gamelog_file_unzipped() + \
                                           "/GL2013.TXT"))

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

    def test_clean_used_files(self):
        r2013.download() # assume works
        r2013.unzip() # assume works 

        # Are the files there before we begin?
        for path in eventfiles2013:
            self.assertTrue(os.path.isfile(r2013.get_dest_unzipped() + \
                                          "/events2013/" + path))
        # Clean 'em' out and check that theyre gone
        r2013.clean_used_files()
        for path in eventfiles2013:
            self.assertFalse(os.path.isfile(r2013.get_dest_unzipped() + \
                                            "/events2013/" + path))
            
    def tearDown(self):
        # Clean out zipped file folder afterwards
        zippedFileFolder = Data.rootDir + Data.defaultDestZippedSuffix
        os.chdir(zippedFileFolder)
        for file in os.listdir(os.getcwd()): 
          if os.path.isdir(file): 
            shutil.rmtree(file)
          else: 
            os.remove(file) 

        # Clean out unzipped file folder as well
        unzippedFileFolder = Data.rootDir + Data.defaultDestUnzippedSuffix
        os.chdir(unzippedFileFolder)
        for file in os.listdir(os.getcwd()): 
          if os.path.isdir(file): 
            shutil.rmtree(file)
          else: 
            os.remove(file) 