import unittest
import os
import shutil

from data import Data
from bot import Bot

from g import *

# @unittest.skip("Focus is not in Bot right now")
class TestBot(unittest.TestCase):

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
    
    def test_incr_streak_length_and_get_streak_length(self):
        for i in range(4):
            bot1.incr_streak_length()
            bot2.incr_streak_length(2)
        self.assertEqual(bot1.get_streak_length(), 4)
        self.assertEqual(bot2.get_streak_length(), 8)

    def test_get_index(self):
        self.assertEqual(bot1.get_index(), 1)
        self.assertEqual(bot2.get_index(), 2)

    def test_choose_player_and_get_player(self):
        bot1.choose_player(p2)
        bot2.choose_player(p4)

        self.assertNotEqual(bot1.get_player(), p4)
        self.assertEqual(bot1.get_player(), p2)
        self.assertNotEqual(bot2.get_player(), p2)
        self.assertEqual(bot2.get_player(), p4)

    def test_get_player_history(self):
        bot3 = Bot(3)
        bot3.choose_player(p1)
        bot3.choose_player(p3)
        bot3.choose_player(p2)
        bot3.choose_player(p4)

        self.assertEqual(bot3.get_player_history(), [p1, p3, p2, p4])