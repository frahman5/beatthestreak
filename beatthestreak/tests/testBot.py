import unittest

from datetime import date

from beatthestreak.filepath import Filepath
from beatthestreak.bot import Bot
from beatthestreak.player import Player
from beatthestreak.tests import setup, teardown, p1, p2, p3, p4, p5
from beatthestreak.exception import MulliganException

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

    def test_update_history_and_get_player_sans_mulligan(self):
        ## All three phases test that correct player and date were assigned 

        # test that passing True for hitVal increases streak length by 1
        self.assertEqual(self.bot1.get_streak_length(), 0) 
        self.bot1.update_history(p2, True, date(2003,3,3))
        self.assertEqual(self.bot1.get_history()[0], 
            (p2, True, date(2003, 3, 3), 1, None))
        self.assertEqual(self.bot1.get_player(), p2) # right player
        self.assertEqual(self.bot1.get_streak_length(), 1) # right streak length
        self.assertEqual(self.bot1.get_max_streak_length(), 1) # right max streak length

        # test that passing 'pass' for hitVal keeps streak length where it is
        suspInvalidOtherS = 'Suspended, Invalid'
        self.assertEqual(self.bot1.get_streak_length(), 1)
        self.bot1.update_history(p3, 'pass', date(2003, 3, 4), other=suspInvalidOtherS)
        self.assertEqual(self.bot1.get_history()[1], 
            (p3, 'pass', date(2003, 3, 4), 1, suspInvalidOtherS))
        self.assertEqual(self.bot1.get_player(), p3) # right player
        self.assertEqual(self.bot1.get_streak_length(), 1) # right streak length
        self.assertEqual(self.bot1.get_max_streak_length(), 1) # right max streak length


        # test that passing False for hitval resets streak length
        self.assertEqual(self.bot1.get_streak_length(), 1)
        self.bot1.update_history(p4, False, date(2003, 3, 5))
        self.assertEqual(self.bot1.get_history()[2], 
            (p4, False, date(2003, 3, 5), 0, None))
        self.assertEqual(self.bot1.get_player(), p4) # right player
        self.assertEqual(self.bot1.get_streak_length(), 0) # right streak length
        self.assertEqual(self.bot1.get_max_streak_length(), 1) # right max streak length

    def test_update_history_with_mulligan(self):
        testDate = date(2003, 4, 1) 
        mulliganRange = (10, 11, 12, 13, 14, 15)
        outsideMulliganRange = [i for i in range(0,151) if i not in mulliganRange]

    ## Case 1: Bot has mulligan    
        for testRange in (outsideMulliganRange, mulliganRange):
            for i in testRange:
                botTrue, botFalse, botPass = Bot(0), Bot(1), Bot(2)
                # streak = 0, hasMulligan = True
                botTrue.claim_mulligan()
                botFalse.claim_mulligan()
                botPass.claim_mulligan()

                # streak = i
                botTrue.incr_streak_length(amount=i)
                botFalse.incr_streak_length(amount=i)
                botPass.incr_streak_length(amount=i)

                # True bot gets a True, False bot gets a False, Pass bot
                # gets a Pass. 
                botTrue.update_history(p1, True, testDate)
                botFalse.update_history(p1, False, testDate)
                botPass.update_history(p1, 'pass', testDate)

                # In both subcases, True bot ups streak length, retains mulligan
                self.assertEqual(botTrue.get_streak_length(), i+1)
                self.assertTrue(botTrue.get_mulligan_status())
                # Pass bot retains streak, retains mulligan
                self.assertEqual(botPass.get_streak_length(), i)
                self.assertTrue(botPass.get_mulligan_status())

                # Subcase 1.1: Streak in [0, 9] or [16,150]
                if testRange == outsideMulliganRange: 
                    # False bot resets streak, retains mulligan
                    self.assertEqual(botFalse.get_streak_length(), 0)
                    self.assertTrue(botFalse.get_mulligan_status())
                    
                # Subcase 1.2: Streak in [10, 15]
                if testRange == mulliganRange:
                    # False bot retains streak length, loses mulligan
                    self.assertEqual(botFalse.get_streak_length(), i)
                    self.assertFalse(botFalse.get_mulligan_status())
        
    ## Case 2: Bot does not have mulligan
        for testRange in (outsideMulliganRange, mulliganRange):
            for i in testRange:
                # streak = 0, hasMulligan = False
                botTrue, botFalse, botPass = Bot(0), Bot(1), Bot(2)
                
                # streak = i
                botTrue.incr_streak_length(amount=i)
                botFalse.incr_streak_length(amount=i)
                botPass.incr_streak_length(amount=i)

                # True bot gets a True, False bot gets a False, Pass bot
                # gets a Pass. 
                botTrue.update_history(p1, True, testDate)
                botFalse.update_history(p1, False, testDate)
                botPass.update_history(p1, 'pass', testDate)

                # True bot always ups streak length, has no mulligan
                self.assertEqual(botTrue.get_streak_length(), i+1)
                self.assertFalse(botTrue.get_mulligan_status())
                # Pass bot always retains streak, has no mulligan
                self.assertEqual(botPass.get_streak_length(), i)
                self.assertFalse(botPass.get_mulligan_status()) 
                # Fail bot always resets streak, has no mulligan
                self.assertEqual(botFalse.get_streak_length(), 0)
                self.assertFalse(botFalse.get_mulligan_status())   

    ## Case 3: If a bot used its mulligan, and gets its streak back to [10,15]
        mulStreakLength = 13
        # streak = 13, hasMulligan = True
        botTrue, botFalse, botPass = Bot(0), Bot(1), Bot(2)
        for bot in (botTrue, botFalse, botPass):
            bot.incr_streak_length(amount = mulStreakLength)
            bot.claim_mulligan()

        # bots use mulligan
        for bot in (botTrue, botFalse, botPass):
            # check streak length and mulligan status before updating
            self.assertEqual(bot.get_streak_length(), mulStreakLength)
            self.assertTrue(bot.get_mulligan_status())

            # after update--> same streak length, no more mulligan
            bot.update_history(p1, False, testDate)
            self.assertEqual(bot.get_streak_length(), mulStreakLength)
            self.assertFalse(bot.get_mulligan_status())

            # after update -> streak dead, stil no mulligan
            bot.update_history(p1, False, testDate)
            self.assertEqual(bot.get_streak_length(), 0)
            self.assertFalse(bot.get_mulligan_status())

        # bot gets its streak length back to [10,15] after resetting to 0
        for length in xrange(10, 16):
            for bot in (botTrue, botFalse, botPass):
                bot.reset_streak()
                bot.incr_streak_length(amount=length)
            # update histories
            botTrue.update_history(p1, True, testDate)
            botFalse.update_history(p1, False, testDate)
            botPass.update_history(p1, 'pass', testDate)
            # True bot ups streak length, has no mulligan
            self.assertEqual(botTrue.get_streak_length(), length+1)
            self.assertFalse(botTrue.get_mulligan_status())
            # Pass bot retains streak, has no mulligan
            self.assertEqual(botPass.get_streak_length(), length)
            self.assertFalse(botPass.get_mulligan_status()) 
            # Fail bot resets streak, has no mulligan
            self.assertEqual(botFalse.get_streak_length(), 0)
            self.assertFalse(botFalse.get_mulligan_status())   



    def test_get_history(self):
        bot3 = Bot(3)
        bot3.update_history(p1, False, date(2003,3,3))
        bot3.update_history(p3, True, date(2003,3,4))
        bot3.update_history(p2, True, date(2003,3,5), other='Suspended, Valid')
        bot3.update_history(p4, False, date(2003,3,6))

        self.assertEqual(bot3.get_history(), [(p1, False, date(2003,3,3), 0, None),
                        (p3, True, date(2003,3,4), 1, None), 
                        (p2, True, date(2003,3,5), 2, 'Suspended, Valid'), 
                        (p4, False, date(2003,3,6), 0, None)])

    def test_activate_mulligan_and_get_mulligan_status(self):
        bot = Bot(0)
        self.assertFalse(bot.get_mulligan_status())

        # activate the mulligan
        bot.claim_mulligan()
        self.assertTrue(bot.get_mulligan_status())

        # trying to claim a mulligan twice should raise an error whether it ...
            # hasn't used its mulligan yet
        self.assertRaises(MulliganException, bot.claim_mulligan)
            # has used its mulligan
        bot.hasMulligan = False
        self.assertRaises(MulliganException, bot.claim_mulligan)
        
