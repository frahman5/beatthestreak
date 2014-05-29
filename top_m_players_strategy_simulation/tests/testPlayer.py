import unittest
from player import Player
from g import *

class testPlayer(unittest.TestCase):
    pass
    # def test_get_and_set_retrosheet_id(self):
    #     self.assertEqual(p1.get_retrosheet_id(), "jacke001")
    #     self.assertEqual(p2.get_retrosheet_id(), "reyej001")

    # def test_get_and_set_teams(self):
    #     self.assertEqual(p1.get_teams(),["WAS"])
    #     self.assertEqual(p2.get_teams(),["MIA"])
    #     self.assertEqual(p3.get_teams(),["CHA", "SLN"])

    # def test_did_start(self):
    #     self.assertFalse(p1.did_start(date(2012, 4, 15)))
    #     self.assertTrue(p2.did_start(date(2012, 4, 15)))

    # def test_find_home_team(self):
    #     self.assertEqual(p1.find_home_team(date(2012, 5, 2)), "WAS")
    #     self.assertEqual(p2.find_home_team(date(2012, 6, 15)), "TBA")

    # def test_did_get_hit(self):
    #     self.assertFalse(p1.did_get_hit(date(2012, 5, 2)))
    #     self.assertFalse(p2.did_get_hit(date(2012, 6, 15)))
    #     self.assertTrue(p2.did_get_hit(date(2012, 6, 16)))

    # def test_get_index(self):
    #     self.assertEqual(p1.get_index(), 1)
    #     self.assertEqual(p2.get_index(), 2)
    
    # def test_get_name(self):
    #     self.assertTrue(p1.get_name(), "Edwin Jackson")
    #     self.assertTrue(p2.get_name(),"Jose Reyes")
    
    # def test_get_bat_ave(self):
    #     self.assertEqual(p1.get_bat_ave(),p1BattingAve)
    #     self.assertEqual(p2.get_bat_ave(),p2BattingAve)