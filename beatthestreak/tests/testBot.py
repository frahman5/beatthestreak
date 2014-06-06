import unittest

from datetime import date

from beatthestreak.filepath import Filepath
from beatthestreak.bot import Bot
from beatthestreak.player import Player
from beatthestreak.tests import setup, teardown, p1, p2, p3, p4, p5

class TestBot(unittest.TestCase):

    def setUp(self):
        self.bot1 = Bot(1)
        self.bot2 = Bot(2)
        setup()
        
    def tearDown(self):
        teardown()
    
    def test_bot_equality(self):
        manny = Player(0, "Manny", "Ramirez", 2010)
        alfonso = Player(1, "Alfonso", "Soriano", 2010)
        self.assertEqual(self.bot1, self.bot2) # empty bots are equal

        # bots with identical histories and max streak lengths are equal
        self.bot1.update_history(manny, True, date(2010, 9, 3))
        self.bot2.update_history(manny, True, date(2010, 9, 3))
        self.assertTrue(self.bot1 == self.bot2)

        # bots with nonidentical histories are unequal
        self.bot1.update_history(alfonso, True, date(2010, 9, 4))
        self.bot2.update_history(manny, True, date(2010, 9, 4))
        self.assertFalse(self.bot1 == self.bot2)

        # bots with unequal max lengths are unequal
        self.bot1.update_history(alfonso, False, date(2010, 9, 5))
        self.bot2.update_history(manny, True, date(2010, 9, 5))
        self.assertFalse(self.bot1 == self.bot2)

    def test_incr_streak_length_and_get_streak_length(self):
        for i in range(4):
            self.bot1.incr_streak_length()
            self.bot2.incr_streak_length(2)
        self.assertEqual(self.bot1.get_streak_length(), 4)
        self.assertEqual(self.bot2.get_streak_length(), 8)

    def test_get_index(self):
        self.assertEqual(self.bot1.get_index(), 1)
        self.assertEqual(self.bot2.get_index(), 2)

    def test_update_history_and_get_player(self):
        ## All three phases test that correct player and date were assigned 

        # test that passing True for hitVal increases streak length by 1
        self.assertEqual(self.bot1.get_streak_length(), 0) 
        self.bot1.update_history(p2, True, date(2003,3,3))
        self.assertEqual(self.bot1.get_player(), p2) # right player
        self.assertEqual(self.bot1.get_streak_length(), 1) # right streak length
        self.assertEqual(self.bot1.get_history()[0][2], date(2003, 3, 3)) # right date

        # test that passing 'pass' for hitVal keeps streak length where it is
        self.assertEqual(self.bot1.get_streak_length(), 1)
        self.bot1.update_history(p3, 'pass', date(2003, 3, 4))
        self.assertEqual(self.bot1.get_player(), p3) # right player
        self.assertEqual(self.bot1.get_streak_length(), 1) # right streak length
        self.assertEqual(self.bot1.get_history()[1][2], date(2003, 3, 4)) # right date

        # test that "pass" False for hitval resets streak length
        self.assertEqual(self.bot1.get_streak_length(), 1)
        self.bot1.update_history(p4, False, date(2003, 3, 5))
        self.assertEqual(self.bot1.get_player(), p4) # right player
        self.assertEqual(self.bot1.get_streak_length(), 0) # right streak length
        self.assertEqual(self.bot1.get_history()[2][2], date(2003, 3, 5)) # right date

    def test_get_history(self):
        bot3 = Bot(3)
        bot3.update_history(p1, False, date(2003,3,3))
        bot3.update_history(p3, True, date(2003,3,4))
        bot3.update_history(p2, True, date(2003,3,5))
        bot3.update_history(p4, False, date(2003,3,6))

        self.assertEqual(bot3.get_history(), [(p1, False, date(2003,3,3), 0),
                        (p3, True, date(2003,3,4), 1), 
                        (p2, True, date(2003,3,5), 2), 
                        (p4, False, date(2003,3,6), 0)])