import unittest
import os
import shutil

from beatthestreak.player import Player, PlayerL
from beatthestreak.tests import setup, teardown, p1, p2, p3, p4, p5, \
     p1BattingAve, p2BattingAve, p3BattingAve, p4BattingAve, p5BattingAve
from beatthestreak.filepath import Filepath
from beatthestreak.exception import NoPlayerException

# @unittest.skip("Focus is not on Player right now")
class testPlayer(unittest.TestCase):
    
    def setUp(self):
        setup()
        
    def tearDown(self):
        teardown()

    def test_get_and_set_retrosheet_id_and_init(self):
        # non MLB player name should raise exception
        self.assertRaises(NoPlayerException, Player, 0, "oogly", "boogly", 1999)
        # player with unique name should be initalized no problem
        self.assertEqual(p1.get_retrosheet_id(), "jacke001")
        # # player with non unique name should initalize sans problem if you
        # # provide a debut date
        self.assertEqual(p2.get_retrosheet_id(), "reyej001")
        # # player with non unique name should initalize with user
        # # help if you don't provide a debut date
        self.assertEqual(Player(0, "Jose", "Reyes", 2005).get_retrosheet_id(), "reyej001")
        ## player initalized from PlayerL should have right data
        pL = Player(0, playerL=PlayerL("jacksed01", 2012))
        self.assertEqual(
            (pL.get_first_name(), pL.get_last_name(), pL.get_bat_ave(), 
                pL.get_lahman_id(), pL.get_retrosheet_id()), 
            (p1.get_first_name(), p1.get_last_name(), p1.get_bat_ave(), 
            p1.get_lahman_id(), p1.get_retrosheet_id()))
        
    def test_eq__(self):
        # test that two similarly made-from-names players are equal
        p1 = Player(0, "Jose", "Reyes", 2012, debut='6/10/2003')
        p2 = Player(1, "Jose", "Reyes", 2010, debut='6/10/2003')
        self.assertEqual(p1, p2)
        # test that a player-from-name and player-from-playerL are equiv
        p3 = PlayerL("reyesjo01", 2010)
        p3 = Player(0, playerL=p3)
        self.assertEqual(p1, p3)

    def test__repr__and__str__(self):
        self.assertEqual(str(p1), "Edwin Jackson: 0.228")
        self.assertEqual("%r" % p1, "Edwin Jackson: 0.228")
        
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
        