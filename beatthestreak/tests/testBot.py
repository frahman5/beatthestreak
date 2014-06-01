import unittest
import os
import shutil

from data import Data
from bot import Bot

from tests import setup, teardown, p1, p2, p3, p4, p5

# @unittest.skip("Focus is not in Bot right now")
class TestBot(unittest.TestCase):

    def setUp(self):
        self.bot1 = Bot(1)
        self.bot2 = Bot(2)
        setup()
        
    def tearDown(self):
        teardown()
    
    def test_incr_streak_length_and_get_streak_length(self):
        for i in range(4):
            self.bot1.incr_streak_length()
            self.bot2.incr_streak_length(2)
        self.assertEqual(self.bot1.get_streak_length(), 4)
        self.assertEqual(self.bot2.get_streak_length(), 8)

    def test_get_index(self):
        self.assertEqual(self.bot1.get_index(), 1)
        self.assertEqual(self.bot2.get_index(), 2)

    def test_assign_player_and_get_player(self):
        self.bot1.assign_player(p2, True)
        self.bot2.assign_player(p4, False)

        self.assertNotEqual(self.bot1.get_player(), p4)
        self.assertEqual(self.bot1.get_player(), p2)
        self.assertNotEqual(self.bot2.get_player(), p2)
        self.assertEqual(self.bot2.get_player(), p4)

    def test_get_player_history(self):
        bot3 = Bot(3)
        bot3.assign_player(p1, False)
        bot3.assign_player(p3, True)
        bot3.assign_player(p2, True)
        bot3.assign_player(p4, False)

        self.assertEqual(bot3.get_player_history(), [(p1, False),
                        (p3, True), (p2, True), (p4, False)])