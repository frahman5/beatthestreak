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
    	# Edwin Jackon test
        self.assertFalse(r1.did_get_hit(date(2012, 5, 2), p1))

        # Jose Reyes Tests
        self.assertTrue(r1.did_get_hit(date(2012, 6, 16), p2))
        self.assertTrue(r1.did_get_hit(date(2005, 4, 4), p2))
        self.assertTrue(r1.did_get_hit(date(2003, 7, 12), p2))
        self.assertFalse(r1.did_get_hit(date(2012, 6, 15), p2))
        self.assertFalse(r1.did_get_hit(date(2008, 9, 21), p2))

        # Alfonso Soriano Tests
        self.assertTrue(r1.did_get_hit(date(2003, 3, 31), p3))
        self.assertTrue(r1.did_get_hit(date(2009, 5, 12), p3))
        self.assertFalse(r1.did_get_hit(date(2001, 9, 4), p3))
        self.assertFalse(r1.did_get_hit(date(2007, 7, 20), p3))
        self.assertFalse(r1.did_get_hit(date(2004, 9, 16), p3))

        # Jorge Posada tests
        self.assertTrue(r1.did_get_hit(date(2004, 8, 17), p4))
        self.assertTrue(r1.did_get_hit(date(2010, 7, 11), p4))
        self.assertFalse(r1.did_get_hit(date(1997, 5, 23), p4))
        self.assertFalse(r1.did_get_hit(date(2000, 4, 30), p4))

        # Manny Ramirez tests (traded in 2008. This test checks to see
        # 	if did_get_hit works for players in a year they are traded)
        self.assertTrue(r1.did_get_hit(date(1994, 7, 26), p5))
        self.assertTrue(r1.did_get_hit(date(2008, 5, 22), p5))
        self.assertTrue(r1.did_get_hit(date(2008, 8, 1), p5))
        self.assertFalse(r1.did_get_hit(date(1995, 6, 30), p5))
        self.assertFalse(r1.did_get_hit(date(2008, 7, 29), p5))
        self.assertFalse(r1.did_get_hit(date(2008, 8, 31), p5))

        # Double Header tests (its a hit iff player got a hit in first game)
        self.assertFalse(r1.did_get_hit(date(1996, 9, 25), p4)) # T1, H2
        self.assertFalse(r1.did_get_hit(date(2008, 9, 7), p2)) # T1, T2
        self.assertTrue(r1.did_get_hit(date(2007, 7, 28), p2)) # H1, T2
        self.assertTrue(r1.did_get_hit(date(2006, 6, 3), p2)) # H1, H2

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