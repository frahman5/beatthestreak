import unittest
import random

from datetime import date

from beatthestreak.filepath import Filepath
from beatthestreak.bot import Bot
from beatthestreak.player import Player
from beatthestreak.tests import setup, teardown, p1, p2, p3, p4, p5
from beatthestreak.exception import MulliganException
from beatthestreak.researcher import Researcher

class TestBot(unittest.TestCase):

    def setUp(self):
        self.bot1 = Bot(1)
        self.bot2 = Bot(2)
        setup()
        
    def tearDown(self):
        teardown()
    
    def test_bot_equality(self):
        manny = Player("Manny", "Ramirez", 2010)
        alfonso = Player("Alfonso", "Soriano", 2010)
        Researcher.create_player_hit_info_csv(manny, 2010)
        Researcher.create_player_hit_info_csv(alfonso, 2010)

        # empty bots are equal
        self.assertEqual(self.bot1, self.bot2) 

        # bots with identical histories and max streak lengths are equal
        self.bot1.update_history(p1=manny, date=date(2010, 9, 4)) # got a hit
        self.bot2.update_history(p1=manny, date=date(2010, 9, 4))
        self.assertTrue(self.bot1 == self.bot2)

        # bots with nonidentical histories, but equal maxStreakLengths are unequal
        self.bot1.update_history(p1=alfonso, date=date(2010, 9, 8)) # got a hit
        self.bot2.update_history(p1=manny, date=date(2010, 9, 6)) # got a hit
        self.assertFalse(self.bot1 == self.bot2)

        # bots with unequal max lengths are unequal
        self.bot1.update_history(p1=alfonso, date=date(2010, 9, 12)) # got a hit
        self.bot2.update_history(p1=manny, date=date(2010, 9, 7))   # didn't get a hit
        self.assertFalse(self.bot1 == self.bot2)

    def test_incr_streak_length_and_get_streak_length(self):
        for i in range(4):
            self.bot1.incr_streak_length()
            self.assertEqual(self.bot1.get_max_streak_length(), i+1)
            self.bot2.incr_streak_length(2)
            self.assertEqual(self.bot2.get_max_streak_length(), (i+1) * 2)

        # should increment current streak correctly
        self.assertEqual(self.bot1.get_streak_length(), 4)
        self.assertEqual(self.bot2.get_streak_length(), 8)

        # should also have updated max streak length
        self.bot1.reset_streak()
        self.bot2.reset_streak()
        self.assertEqual(self.bot1.get_max_streak_length(), 4)
        self.assertEqual(self.bot2.get_max_streak_length(), 8)

    def test_get_index(self):
        self.assertEqual(self.bot1.get_index(), 1)
        self.assertEqual(self.bot2.get_index(), 2)

    def test_update_history_single_down_no_mulligan(self):

        # test that passing True for hitVal increases streak length by 1
        Researcher.create_player_hit_info_csv(p2, 2003)
        d1 = date(2003, 7, 1) # Jose Reyes (p2) got a hit on this date
        self.assertEqual(self.bot1.get_streak_length(), 0) 
        self.bot1.update_history(p1=p2, date=d1)
        self.assertEqual(self.bot1.get_history()[0], 
            (p2, None, True, None, d1, 1, None))
        self.assertEqual(self.bot1.get_players(), (p2,None)) # right players
        self.assertEqual(self.bot1.get_streak_length(), 1) # right streak length
        self.assertEqual(self.bot1.get_max_streak_length(), 1) # right max streak length

        # test that passing 'pass' for hitVal keeps streak length where it is
        # and other gets updated correctly
        d2 = date(2001, 6, 15)
        Endy = Player("Endy", "Chavez", 2001) # played in suspended, invalid game on d2
        Researcher.create_player_hit_info_csv(Endy, 2001)
        suspInvalidOtherS = 'Suspended-Invalid.'
        self.assertEqual(self.bot1.get_streak_length(), 1)
        self.bot1.update_history(p1=Endy,  date=d2) #p3 got a pass
        self.assertEqual(self.bot1.get_history()[1], 
            (Endy, None, 'pass', None, d2, 1, suspInvalidOtherS))
        self.assertEqual(self.bot1.get_players(), (Endy, None)) # right players
        self.assertEqual(self.bot1.get_streak_length(), 1) # right streak length
        self.assertEqual(self.bot1.get_max_streak_length(), 1) # right max streak length


        # test that passing False for hitval resets streak length
        Researcher.create_player_hit_info_csv(p4, 2003)
        d3 = date(2003, 4, 13) # Jorge Posada (p4) didn't get a hit on this date
        self.assertEqual(self.bot1.get_streak_length(), 1)
        self.bot1.update_history(p1=p4,  date=d3) #p4 got a False
        self.assertEqual(self.bot1.get_history()[2], 
            (p4, None, False, None, d3, 0, None))
        self.assertEqual(self.bot1.get_players(), (p4, None)) # right players
        self.assertEqual(self.bot1.get_streak_length(), 0) # right streak length
        self.assertEqual(self.bot1.get_max_streak_length(), 1) # right max streak length

    def test_update_history_single_down_with_mulligan(self):
        testDate = date(2001, 6, 15)
        pT = Player("Tom", "Goodwin", 2001) # got a hit on testDate
        pF = Player("Troy", "Glaus", 2001) # did not get a hit on testDate
        pP = Player("Endy", "Chavez", 2001) # hot a pass on testDate
        Researcher.create_player_hit_info_csv(pT, 2001)
        Researcher.create_player_hit_info_csv(pF, 2001)
        Researcher.create_player_hit_info_csv(pP, 2001)
        mulliganRange = [10, 11, 12, 13, 14, 15]
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
                botTrue.update_history(p1=pT, date=testDate)
                botFalse.update_history(p1=pF, date=testDate)
                botPass.update_history(p1=pP, date=testDate)

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
                    self.assertFalse(botFalse.has_used_mulligan())

                # Subcase 1.2: Streak in [10, 15]
                if testRange == mulliganRange:
                    # False bot retains streak length, loses mulligan
                    self.assertEqual(botFalse.get_streak_length(), i)
                    self.assertFalse(botFalse.get_mulligan_status())
                    self.assertTrue(botFalse.has_used_mulligan()) 

        ## Case 2: Bot used its mulligan, and gets its streak back to [10,15]
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
            bot.update_history(p1=pF, date=testDate) # failed to get a hit
            self.assertEqual(bot.get_streak_length(), mulStreakLength)
            self.assertFalse(bot.get_mulligan_status())

            # after update -> streak dead, stil no mulligan
            bot.update_history(p1=pF, date=testDate) # failed to get a hit
            self.assertEqual(bot.get_streak_length(), 0)
            self.assertFalse(bot.get_mulligan_status())

        # bot gets its streak length back to [10,15] after resetting to 0
        for length in xrange(10, 16):
            for bot in (botTrue, botFalse, botPass):
                bot.reset_streak()
                bot.incr_streak_length(amount=length)
            # update histories
            botTrue.update_history(p1=pT, date=testDate)
            botFalse.update_history(p1=pF, date=testDate)
            botPass.update_history(p1=pP, date=testDate)
            # True bot ups streak length, has no mulligan
            self.assertEqual(botTrue.get_streak_length(), length+1)
            self.assertFalse(botTrue.get_mulligan_status())
            self.assertTrue(botTrue.has_used_mulligan())
            # Pass bot retains streak, has no mulligan
            self.assertEqual(botPass.get_streak_length(), length)
            self.assertFalse(botPass.get_mulligan_status()) 
            self.assertTrue(botTrue.has_used_mulligan())
            # Fail bot resets streak, has no mulligan
            self.assertEqual(botFalse.get_streak_length(), 0)
            self.assertFalse(botFalse.get_mulligan_status())   
            self.assertTrue(botFalse .has_used_mulligan())

        ## Loose ends to get 100% test coverage
        ## A mulligan eligble bot with a player who did not get a hit in a
        ## suspended, valid game creates the correct "otherInfo"
        Rafael = Player("Rafael", "Furcal", 2010) # no hit in suspended, valid game
        Researcher.create_player_hit_info_csv(Rafael, 2011)
        bot = Bot(0)
        bot.claim_mulligan()
        bot.incr_streak_length(amount=13)
        bot.update_history(p1=Rafael, date=date(2011, 4, 8))
        self.assertEqual(bot.get_history()[0][6], 'Suspended-Valid. Mulligan.')

    def test_update_history_double_down_no_mulligan(self):
        d1 = date(2001, 6, 15)
        # initalize pseudo-random number generator
        random.seed()

        # two players that got hits on d1
        pH1 = Player("Derek", "Jeter", 2001)
        pH2 = Player("Rafael", "Furcal", 2001)
        # two players that did not get hits on d1
        pF1 = Player("Rickey", "Henderson", 2001)
        pF2 = Player("Shane", "Halter", 2001)
        # two players that got passes on d1
        pP1 = Player("Endy", "Chavez", 2001) # played in suspended, invalid game on d1
        pP2 = Player("Mark", "Loretta", 2001) #played in suspended, invalid game on d1

        ## Create player hit info csv's
        for player in (pH1, pH2, pF1, pF2, pP1, pP2):
            Researcher.create_player_hit_info_csv(player, 2001)

        ## Case 1: p1 Hit, p2 No Hit : Streak ups 2 (maxStreak may change)
        bot = Bot(10)
        maxStreak = 0 # manually keep track of maxStreak
        for i in range(5):
            # set the bot streak to a pseudo-random number
            startLen = random.randint(0,100)
            if startLen + 2 > maxStreak:
                maxStreak = startLen + 2
            bot.reset_streak()
            bot.incr_streak_length(amount=startLen)
            self.assertEqual(bot.get_streak_length(), startLen)

            # update the history and check that it updated correctly
            bot.update_history(p1=pH1, p2=pH2, date=d1)
            self.assertEqual(bot.get_history()[i], # right history
                (pH1, pH2, True, True, d1, startLen+2, None))
            self.assertEqual(bot.get_streak_length(), startLen + 2) # right streak length
            self.assertEqual(bot.get_players(), (pH1, pH2)) # right players
            self.assertEqual(bot.get_max_streak_length(), maxStreak)

        ## Case 2: p1 No Hit, p2 No Hit : Streak resets (maxStreak may change at incr_streak_length)
        bot = Bot(10)
        maxStreak = 0 # manually keep track of maxStreak
        for i in range(5):
            # set the bot streak to a pseudo-random number
            startLen = random.randint(0,100)
            bot.reset_streak()
            bot.incr_streak_length(amount=startLen)
            if startLen > maxStreak:
                maxStreak = startLen
            self.assertEqual(bot.get_streak_length(), startLen)

            # update the history and check that it updated correctly
            bot.update_history(p1=pF1, p2=pF2, date=d1)
            self.assertEqual(bot.get_history()[i], # right history
                (pF1, pF2, False, False, d1, 0, None))
            self.assertEqual(bot.get_streak_length(), 0) # right streak length
            self.assertEqual(bot.get_players(), (pF1, pF2)) # right players
            self.assertEqual(bot.get_max_streak_length(), maxStreak)

        ## Case 3: p1 pass, p2 pass : Streak stagnant (maxStreak may change at incr_streak_length)
        bot = Bot(10)
        maxStreak = 0 # manually keep track of maxStreak
        for i in range(5):
            # set the bot streak to a pseudo-random number
            startLen = random.randint(0,100)
            bot.reset_streak()
            bot.incr_streak_length(amount=startLen)
            if startLen > maxStreak:
                maxStreak = startLen
            self.assertEqual(bot.get_streak_length(), startLen)

            # update the history and check that it updated correctly
            bot.update_history(p1=pP1, p2=pP2, date=d1)
            self.assertEqual(bot.get_history()[i], # right history
                (pP1, pP2, 'pass', 'pass', d1, startLen, 'Suspended-Invalid.' +\
                    ' Suspended-Invalid.'))
            self.assertEqual(bot.get_streak_length(), startLen) # right streak length
            self.assertEqual(bot.get_players(), (pP1, pP2)) # right players
            self.assertEqual(bot.get_max_streak_length(), maxStreak)

        ## Case 3.1: p1 Hit, p2 No Hit : Streak resets (maxStreak may change at incr_streak_length)
        bot = Bot(10)
        maxStreak = 0 # manually keep track of maxStreak
        for i in range(5):
            # set the bot streak to a pseudo-random number
            startLen = random.randint(0,100)
            bot.reset_streak()
            bot.incr_streak_length(amount=startLen)
            if startLen > maxStreak:
                maxStreak = startLen
            self.assertEqual(bot.get_streak_length(), startLen)

            # update the history and check that it updated correctly
            bot.update_history(p1=pH1, p2=pF1, date=d1)
            self.assertEqual(bot.get_history()[i], # right history
                (pH1, pF1, True, False, d1, 0, None))
            self.assertEqual(bot.get_streak_length(), 0) # right streak length
            self.assertEqual(bot.get_players(), (pH1, pF1)) # right players
            self.assertEqual(bot.get_max_streak_length(), maxStreak)

        ## Case 3.2: p1 No hit, p2 Hit : Streak resets (maxStreak may change at incr_streak_length)
        bot = Bot(10)
        maxStreak = 0 # manually keep track of maxStreak
        for i in range(5):
            # set the bot streak to a psedo-random number
            startLen = random.randint(0,100)
            bot.reset_streak()
            bot.incr_streak_length(amount=startLen)
            if startLen > maxStreak:
                maxStreak = startLen
            self.assertEqual(bot.get_streak_length(), startLen)

            # update the history and check that it updated correctly
            bot.update_history(p1=pF2, p2=pH1, date=d1)
            self.assertEqual(bot.get_history()[i], # right history
                (pF2, pH1, False, True, d1, 0, None))
            self.assertEqual(bot.get_streak_length(), 0) # right streak length
            self.assertEqual(bot.get_players(), (pF2, pH1)) # right players
            self.assertEqual(bot.get_max_streak_length(), maxStreak)

        ## Case 4.1: p1 Hit, p2 Pass : Streak ups 1 (maxStreak may change)
        bot = Bot(10)
        maxStreak = 0 # manually keep track of maxStreak
        for i in range(5):
            # set the bot streak to a pseudo-random number
            startLen = random.randint(0,100)
            if startLen + 1 > maxStreak:
                maxStreak = startLen + 1
            bot.reset_streak()
            bot.incr_streak_length(amount=startLen)
            self.assertEqual(bot.get_streak_length(), startLen)

            # update the history and check that it updated correctly
            bot.update_history(p1=pH2, p2=pP1, date=d1)
            self.assertEqual(bot.get_history()[i], # right history
                (pH2, pP1, True, 'pass', d1, startLen+1, 'Suspended-Invalid.'))
            self.assertEqual(bot.get_streak_length(), startLen + 1) # right streak length
            self.assertEqual(bot.get_players(), (pH2, pP1)) # right players
            self.assertEqual(bot.get_max_streak_length(), maxStreak)

        ## Case 4.2: p1 pass, p2 Hit : Streak ups 1 (maxStreak may change)
        bot = Bot(10)
        maxStreak = 0
        for i in range(5):
            # set the bot streak to a pseudo-random number
            startLen = random.randint(0,100)
            if startLen + 1 > maxStreak:
                maxStreak = startLen + 1
            bot.reset_streak()
            bot.incr_streak_length(amount=startLen)
            self.assertEqual(bot.get_streak_length(), startLen)

            # update the history and check that it updated correctly
            bot.update_history(p1=pP2, p2=pH1, date=d1)
            self.assertEqual(bot.get_history()[i], # right history
                (pP2, pH1, 'pass', True, d1, startLen+1, 'Suspended-Invalid.'))
            self.assertEqual(bot.get_streak_length(), startLen + 1) # right streak length
            self.assertEqual(bot.get_players(), (pP2, pH1)) # right players
            self.assertEqual(bot.get_max_streak_length(), maxStreak)

        ## Case 5.1: p1 No Hit, p2 Pass : Streak resets (maxStreak may change at incr_streak_length)
        bot = Bot(10)
        maxStreak = 0 # manually keep track of max streak
        for i in range(5):
            # set the bot streak to a psedo-random number
            startLen = random.randint(0,100)
            bot.reset_streak()
            bot.incr_streak_length(amount=startLen)
            if startLen > maxStreak:
                maxStreak = startLen
            self.assertEqual(bot.get_streak_length(), startLen)

            # update the history and check that it updated correctly
            bot.update_history(p1=pF1, p2=pP1, date=d1)
            self.assertEqual(bot.get_history()[i], # right history
                (pF1, pP1, False, 'pass', d1, 0, 'Suspended-Invalid.'))
            self.assertEqual(bot.get_streak_length(), 0) # right streak length
            self.assertEqual(bot.get_players(), (pF1, pP1)) # right players
            self.assertEqual(bot.get_max_streak_length(), maxStreak)

        ## Case 5.2: p1 Pass, p2 No hit: Streak resets (maxStreak may change at incr_streak_length)
        bot = Bot(10)
        maxStreak = 0 # manually keep track of max streak
        for i in range(5):
            # set the bot streak to a psedo-random number
            startLen = random.randint(0,100)
            bot.reset_streak()
            bot.incr_streak_length(amount=startLen)
            if startLen > maxStreak:
                maxStreak = startLen
            self.assertEqual(bot.get_streak_length(), startLen)

            # update the history and check that it updated correctly
            bot.update_history(p1=pP2, p2=pF2, date=d1)
            self.assertEqual(bot.get_history()[i], # right history
                (pP2, pF2, 'pass', False, d1, 0, 'Suspended-Invalid.'))
            self.assertEqual(bot.get_streak_length(), 0) # right streak length
            self.assertEqual(bot.get_players(), (pP2, pF2)) # right players
            self.assertEqual(bot.get_max_streak_length(), maxStreak)

    def test_update_history_double_down_with_mulligan(self):
        d1 = date(2001, 6, 15)
        sGD2001 = Researcher.get_sus_games_dict(2001)
        mulliganRange = [10, 11, 12, 13, 14, 15]
        outsideMulliganRange = [i for i in range(0,151) if i not in mulliganRange]

        # two players that got hits on d1
        pH1 = Player("Derek", "Jeter", 2001)
        pH2 = Player("Rafael", "Furcal", 2001)
        # two players that did not get hits on d1
        pF1 = Player("Rickey", "Henderson", 2001)
        pF2 = Player("Shane", "Halter", 2001)
        # two players that got passes on d1
        pP1 = Player("Endy", "Chavez", 2001) # played in suspended, invalid game on d1
        pP2 = Player("Mark", "Loretta", 2001) #played in suspended, invalid game on d1

        # initalize pseudo-random number generator
        random.seed()

        ## Case 1: Bot has mulligan    
        for testRange in (outsideMulliganRange, mulliganRange):
            for i in testRange:
                botHH, botFF, botPP = Bot(0), Bot(1), Bot(2)
                botHF, botFH, botHP = Bot(3), Bot(4), Bot(5)
                botPH, botFP, botPF = Bot(6), Bot(7), Bot(9)

                bots = (
                    botHH, botFF, botPP, 
                    botHF, botFH, 
                    botHP, botPH, 
                    botFP, botPF )

                # streak = 0, hasMulligan = True
                for bot in bots:
                    bot.claim_mulligan()

                # streak = i
                for bot in bots:
                    bot.reset_streak()
                    bot.incr_streak_length(amount=i)

                # Bots update histories
                botHH.update_history(p1=pH1, p2=pH2, date=d1)
                botFF.update_history(p1=pF1, p2=pF2, date=d1)
                botPP.update_history(p1=pP1, p2=pP2, date=d1)

                botHF.update_history(p1=pH1, p2=pF1, date=d1)
                botFH.update_history(p1=pF1, p2=pH2, date=d1)

                botHP.update_history(p1=pH1, p2=pP1, date=d1)
                botPH.update_history(p1=pP2, p2=pH1, date=d1)

                botFP.update_history(p1=pF1, p2=pP2, date=d1)
                botPF.update_history(p1=pP1, p2=pF1, date=d1)


                # In both subcases, botHH, botHP, botPH, and botPP have same result
                    # bot HH : streak ups 2, retain mulligan
                self.assertEqual(botHH.get_streak_length(), i+2)
                self.assertTrue(botHH.get_mulligan_status())
                    # bot HP : streak ups 1, retain mulligan
                self.assertEqual(botHP.get_streak_length(), i+1)
                self.assertTrue(botHP.get_mulligan_status())
                    # bot PH : streak ups 1, retain mulligan
                self.assertEqual(botPH.get_streak_length(), i+1)
                self.assertTrue(botPH.get_mulligan_status())
                    # bot PP : streak stagnant, retain mulligan
                self.assertEqual(botPP.get_streak_length(), i)
                self.assertTrue(botPP.get_mulligan_status())

                # Subcase 1.1: Streak in [0, 9] or [16,150]
                if testRange == outsideMulliganRange: 
                    # bots NN, NH, HN, NP, PN : reset streak, retain mulligan
                    for bot in (botFF, botFH, botHF, botFP, botPF):
                        self.assertEqual(bot.get_streak_length(), 0)
                        self.assertTrue(bot.get_mulligan_status())
                    
                # Subcase 1.2: Streak in [10, 15]
                if testRange == mulliganRange:
                    # bots NN, NH, HN, NP, PN : streak stagnant, lose mulligan
                    for bot in (botFF, botFH, botHF, botFP, botPF):
                        self.assertEqual(bot.get_streak_length(), i)
                        self.assertTrue(bot.has_used_mulligan())
                        self.assertFalse(bot.get_mulligan_status())

        ## Case 2: If a bot used its mulligan, and gets its streak back to [10,15]
        mulStreakLength = random.randint(10,15) # 10 <= mulStreakLength <= 15
        # streak in mulliganRange, hasMulligan = True
        botHH, botFF, botPP = Bot(0), Bot(1), Bot(2)
        botHF, botFH, botHP = Bot(3), Bot(4), Bot(5)
        botPH, botFP, botPF = Bot(6), Bot(7), Bot(9)
        bots = (
                    botHH, botFF, botPP, 
                    botHF, botFH, 
                    botHP, botPH, 
                    botFP, botPF )
        for bot in bots:
            bot.claim_mulligan()
            bot.incr_streak_length(amount = mulStreakLength)
            
        # bots use mulligan
        for bot in bots:
            # check streak length and mulligan status before updating
            self.assertEqual(bot.get_streak_length(), mulStreakLength)
            self.assertTrue(bot.get_mulligan_status())

            # after update--> same streak length, no more mulligan
            bot.update_history(p1=pF1, p2=pF2, date=d1) # failed to get a hit
            self.assertEqual(bot.get_streak_length(), mulStreakLength)
            self.assertFalse(bot.get_mulligan_status())
            self.assertTrue(bot.has_used_mulligan())

            # after update -> streak dead, stil no mulligan
            bot.update_history(p1=pF1, p2=pH1, date=d1) # failed to get a hit
            self.assertEqual(bot.get_streak_length(), 0)
            self.assertFalse(bot.get_mulligan_status())
            self.assertTrue(bot.has_used_mulligan)

        # bot gets its streak length back to [10,15] after resetting to 0
        for length in xrange(10, 16):
            for bot in bots:
                bot.reset_streak()
                bot.incr_streak_length(amount=length)

            # Bots update histories
            botHH.update_history(p1=pH1, p2=pH2, date=d1)
            botFF.update_history(p1=pF1, p2=pF2, date=d1)
            botPP.update_history(p1=pP1, p2=pP2, date=d1)

            botHF.update_history(p1=pH1, p2=pF1, date=d1)
            botFH.update_history(p1=pF1, p2=pH2, date=d1)

            botHP.update_history(p1=pH1, p2=pP1, date=d1)
            botPH.update_history(p1=pP2, p2=pH1, date=d1)

            botFP.update_history(p1=pF1, p2=pP2, date=d1)
            botPF.update_history(p1=pP1, p2=pF1, date=d1)

            # bot HH : streak ups 2, has no mulligan
            self.assertEqual(botHH.get_streak_length(), length+2)
            self.assertFalse(botHH.get_mulligan_status())
            self.assertTrue(botHH.has_used_mulligan())

            # bot PP : streak stagnant, has no mulligan
            self.assertEqual(botPP.get_streak_length(), length)
            self.assertFalse(botPP.get_mulligan_status())
            self.assertTrue(botPP.has_used_mulligan())

            # bot HP, PH : streak ups 1, has no mulligan
            for bot in (botHP, botPH):
                self.assertEqual(bot.get_streak_length(), length + 1)
                self.assertFalse(bot.get_mulligan_status())
                self.assertTrue(bot.has_used_mulligan())

            # bot FF, HF, FH, FP, PF : resets streak, has no mulligan
            for bot in (botFF, botHF, botFH, botFP, botPF):
                self.assertEqual(bot.get_streak_length(), 0)
                self.assertFalse(bot.get_mulligan_status())
                self.assertTrue(bot.has_used_mulligan())

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
        
