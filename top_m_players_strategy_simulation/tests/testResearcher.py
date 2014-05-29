import os
import shutil
import unittest

from g import *
from data import Data

# @unittest.skip("Focus is not in Researcher right now")
class TestResearcher(unittest.TestCase):
    
    def setUp(self):
        # Clean out zipped file folder of everything
        zippedFileFolder = Data.rootDir + Data.defaultDestZippedSuffix
        os.chdir(zippedFileFolder)
        for file in os.listdir(os.getcwd()): os.remove(file)

        # Clean out unzipped file folder as well
        unzippedFileFolder = Data.rootDir + Data.defaultDestUnzippedSuffix
        os.chdir(unzippedFileFolder)
        for file in os.listdir(os.getcwd()): 
          if os.path.isdir(file): 
            shutil.rmtree(file)
          else: 
            os.remove(file)

    def test_get_participants(self):
    	self.assertEqual(r1.get_participants(date(2011,9,4)), 
        	             participants_2011_9_4)
        self.assertEqual(r1.get_participants(date(2012,3,28)), 
        	             participants_2012_3_28)
        self.assertEqual(r1.get_participants(date(2013,6,7)), 
        	             participants_2013_6_7)

    def test_find_home_team(self):
    	self.assertEqual(r1.find_home_team(date(2011, 8, 3), p1), "MIL")
        self.assertEqual(r1.find_home_team(date(2012, 5, 2), p1), "WAS")
        self.assertEqual(r1.find_home_team(date(2012, 6, 15), p2), "TBA")
        self.assertEqual(r1.find_home_team(date(2013, 9, 20), p2), "BOS")

    def test_did_start(self):
        self.assertFalse(r1.did_start(date(2011, 7, 2), p1))
        self.assertTrue(r1.did_start(date(2011, 9, 14), p2))
        self.assertFalse(r1.did_start(date(2012, 4, 15), p1))
        self.assertTrue(r1.did_start(date(2012, 4, 15), p2))
        self.assertTrue(r1.did_start(date(2013, 5, 17), p1))
        self.assertTrue(r1.did_start(date(2013, 8, 11), p2))

    def test_did_get_hit(self):
        self.assertFalse(r1.did_get_hit(date(2012, 5, 2), p1))
        self.assertFalse(r1.did_get_hit(date(2012, 6, 15), p2))
        self.assertTrue(r1.did_get_hit(date(2012, 6, 16), p2))

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