import unittest
import os
import shutil

from player import Player
from tests import setup, teardown, p1, p2, p3, p4, p5, p1BattingAve, \
    p2BattingAve, p3BattingAve, p4BattingAve, p5BattingAve
from data import Data

# @unittest.skip("Focus is not on Player right now")
class testPlayer(unittest.TestCase):
    
    def setUp(self):
        tests.setup()
        
    def tearDown(self):
        tests.teardown()

    def test_get_and_set_retrosheet_id(self):
        self.assertEqual(p1.get_retrosheet_id(), "jacke001")
        self.assertEqual(p2.get_retrosheet_id(), "reyej001")

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
        