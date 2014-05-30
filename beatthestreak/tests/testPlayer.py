import unittest
import os
import shutil

from player import Player
from tests import setup, teardown, p1, p2, p3, p4, p5, p1BattingAve, \
    p2BattingAve, p3BattingAve, p4BattingAve, p5BattingAve
from data import Data
from exception import NoPlayerException

# @unittest.skip("Focus is not on Player right now")
class testPlayer(unittest.TestCase):
    
    def setUp(self):
        setup()
        
    def tearDown(self):
        teardown()

    # def test_get_and_set_retrosheet_id(self):
        # non MLB player name should raise exception
        # self.assertRaises(NoPlayerException, Player, 0, "oogly", "boogly", 1999)
        # # player with unique name should be initalized no problem
        # self.assertEqual(p1.get_retrosheet_id(), "jacke001")
        # # # player with non unique name should initalize sans problem if you
        # # # provide a debut date
        # self.assertEqual(p2.get_retrosheet_id(), "reyej001")
        # # # player with non unique name should initalize with user
        # # # help if you don't provide a debut date
        # self.assertEqual(Player(0, "Jose", "Reyes", 2005).get_retrosheet_id(), "reyej001")
        

    def test_get_and_set_lahman_id(self):
        self.assertEqual(p1.get_lahman_id(), "jacksed01")
        self.assertEqual(p2.get_lahman_id(), "reyesjo01")
        self.assertEqual(p3.get_lahman_id(), "soriaal01")
        self.assertEqual(p4.get_lahman_id(), "posadjo01")
        self.assertEqual(p5.get_lahman_id(), "ramirma02")

    def test_get_index(self):
        self.assertEqual(p1.get_index(), 1)
        self.assertEqual(p2.get_index(), 2)
    
    def test_get_name(self):
        self.assertTrue(p1.get_name(), "Edwin Jackson")
        self.assertTrue(p2.get_name(),"Jose Reyes")
    
    def test_get_bat_ave(self):
        self.assertEqual(p1.get_bat_ave(),p1BattingAve)
        self.assertEqual(p2.get_bat_ave(),p2BattingAve)
        self.assertEqual(p3.get_bat_ave(),p3BattingAve)
        self.assertEqual(p4.get_bat_ave(),p4BattingAve)
        self.assertEqual(p5.get_bat_ave(),p5BattingAve)
        