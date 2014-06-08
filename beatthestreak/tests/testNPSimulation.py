import unittest
import os

from datetime import date

from beatthestreak.tests import setup, teardown
from beatthestreak.npsimulation import NPSimulation
from beatthestreak.exception import DifficultYearException
from beatthestreak.player import Player
from beatthestreak.bot import Bot
from beatthestreak.filepath import Filepath


class TestNPSimulation(unittest.TestCase):

    players2003_2002 = \
        [Player(0, "Barry", "Bonds", 2002), Player(1, "Manny", "Ramirez", 2002), 
         Player(2, "Mike", "Sweeney", 2002), Player(3, "Larry", "Walker", 2002), 
         Player(4, "Vladimir", "Guerrero", 2002), Player(5, "Bernie", "Williams", 2002, debut='7/7/1991'), 
         Player(6, "Todd", "Helton", 2002),Player(7, "Chipper", "Jones", 2002), 
         Player(8, "Ichiro", "Suzuki", 2002), Player(9, "Magglio", "Ordonez", 2002),
         Player(10, "Jose", "Vidro", 2002), Player(11, "Albert", "Pujols", 2002),
         Player(12, "Jason", "Giambi", 2002),Player(13, "Jeff", "Kent", 2002),
         Player(14, "Adam", "Kennedy", 2002), Player(15, "Jim", "Edmonds", 2002),
         Player(16, "Nomar", "Garciaparra", 2002), Player(17, "Bobby", "Abreu", 2002), 
         Player(18, "Miguel", "Tejada", 2002), Player(19, "Edgardo", "Alfonzo", 2002)]

    players_2001_2001_N15_P16 = \
        [Player(0, "Ichiro", "Suzuki", 2001), Player(1, "Larry", "Walker", 2001), 
        ]
    def setUp(self):
        setup()
        self.npSim2010_1 = NPSimulation(2010, 2010, 100, 35)
        self.npSim2010_2 = NPSimulation(2010, 2010, 100, 20)
        self.npSim2001_1 = NPSimulation(2001, 2001, 57, 110)
        self.npSim2001_2 = NPSimulation(2001, 2001, 57, 19)
        self.npSim2003_2002 = NPSimulation(2003, 2002, 40, 20)
        self.maxDiff = None
        
    def tearDown(self):
        teardown()

    def test_start_date_in_init(self):
        self.assertEqual(self.npSim2010_1.get_date(), date(2010, 4, 4))
        self.npSim2010WithStartDate = NPSimulation(
            2010, 2010, 100, 35, startDate=date(2010,6,7))
        self.assertEqual(self.npSim2010WithStartDate.get_date(),date(2010,6,7))

    # @unittest.skip("Too long")
    def test_setup(self):
        self.npSim2003_2002.setup() # sets up the simulation

        ## test that players are successfully created
        simPlayers = self.npSim2003_2002.get_players()
        for index, player in enumerate(self.players2003_2002):
            self.assertTrue(player in simPlayers) # check that it gets right players
            # check they are in the right order
            if index == len(self.players2003_2002)-1:
                break
            self.assertGreaterEqual(self.players2003_2002[index].get_bat_ave(), 
                self.players2003_2002[index+1].get_bat_ave())

        ## test that bots are successfully created
        bots = self.npSim2003_2002.get_bots()
        self.assertEqual(len(bots), 40)
        for index, thing in enumerate(bots):
            if index == len(bots)-1:
                break
            self.assertEqual(type(thing), Bot) # its a bot
            self.assertLessEqual(bots[index].get_index(), bots[index+1].get_index()) 
            self.assertTrue(thing.get_mulligan_status()) # has a mulligan

        ## test that min_bat_ave is calculated and initalized correctly
        self.assertEqual(self.npSim2003_2002.get_min_bat_ave(), 0.308)

    @unittest.skip("Too long")
    def test_calc_and_get_min_bat_ave(self): 
        self.npSim2010_1.setup() 
        self.npSim2010_2.setup()
        self.npSim2001_1.setup()
        self.npSim2001_2.setup()
        self.assertEqual(self.npSim2010_1.get_min_bat_ave(), 0.290)
        self.assertEqual(self.npSim2010_2.get_min_bat_ave(), 0.300)
        self.assertEqual(self.npSim2001_1.get_min_bat_ave(), 0.266)
        self.assertEqual(self.npSim2001_2.get_min_bat_ave(), 0.319)
        self.assertRaises(DifficultYearException, NPSimulation, 1981, 1981, 100, 35)
        self.assertRaises(DifficultYearException, NPSimulation, 1950, 1950, 42, 7)

    @unittest.skip("Too long")
    def test_simulate(self):
        # check that test results folder is empty
        self.assertEqual(os.listdir(Filepath.get_results_folder(
            year=2010, test=True)), [])
        # Run the simulation
        self.npSim2010_2.simulate(test=True)
        # Check that the results file is now there
        self.assertTrue(os.path.isfile(Filepath.get_results_file(2010, test=True)))
        
        # Check that the simulation runs in non-test mode as well
        self.npSim2010_2 = NPSimulation(2010, 2010, 100, 20)
        self.npSim2010_2.simulate()

    @unittest.skip("Too long")
    def test_mass_simulate(self):
        # just checks that it runs
        self.npSim2001_1.mass_simulate((2001, 2002), (1, 3), (1, 5), (1, 5), 
            Test=True)

    def test_get_year(self):
        self.assertEqual(self.npSim2010_1.get_sim_year(), 2010)
        self.assertEqual(self.npSim2001_2.get_sim_year(), 2001)

    def test_sim_next_day(self):
        p0, p1, p2, p3, p4, p5, p6, p7, p8, p9 = self.players2003_2002[0:10]
        p10, p11, p12, p13, p14, p15, p16, p17, p18, p19 = self.players2003_2002[10:20]

        self.npSim2003_2002.setup() # assume works
        bots = self.npSim2003_2002.get_bots()

        ####### check that first day works (TEST 1)
        self.npSim2003_2002.sim_next_day()
        self.assertEqual(len(bots), 40) # check that bots are not empty
        self.assertEqual([bot.get_player() for bot in bots], [p14] * 40)
        self.assertEqual([bot.get_streak_length() for bot in bots], [1] * 40)
        self.assertEqual([bot.get_history() for bot in bots], 
            [[(p14, True, date(2003, 3, 30), 1, None)]] * 40)
        self.assertEqual(self.npSim2003_2002.get_date(), date(2003, 3, 31))
        
        ######## check that an arbitrary day-May 14-works (TEST 2)
        self.npSim2003_2002.set_date(date(2003, 5, 14))
        self.npSim2003_2002.sim_next_day()

        botPlayers = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, 
                      p11, p12, p13, p15, p16, p17, p18, p19, p0, p1, 
                      p2, p3, p4, p5, p6, p7, p8, p9, p11, p12, 
                      p13, p15, p16, p17, p18, p19, p0, p1, p2, p3]
        botStreaks = [2,0,2,2,2,2,0,0,2,0, 
                      0,0,2,0,2,2,2,2,2,0,
                      2,2,2,2,0,0,2,0,0,0,
                      2,0,2,2,2,2,2,0,2,2]
        bools = map(lambda x: x > 0, botStreaks)
        botDates = [date(2003, 5, 14)] * 40

        day2resultsRaw = zip(zip(botPlayers, bools), zip(botDates, botStreaks))
        day2results = [(f[0], f[1], s[0], s[1], None) for f, s in day2resultsRaw]
        botPlayerHistories = [[(p14, True, date(2003, 3, 30), 1, None), day2] for \
             day2 in day2results]
             
        self.assertEqual(len(bots), 40) # check that bots are not empty
        self.assertEqual([bot.get_player() for bot in bots], botPlayers)
        self.assertEqual([bot.get_streak_length() for bot in bots], botStreaks)
        self.assertEqual([bot.get_history() for bot in bots], 
                         botPlayerHistories)
        self.assertEqual(self.npSim2003_2002.get_date(), date(2003, 5, 15))
        self.__sim_next_day_t_3()

    def __sim_next_day_t_3(self):
        ##### check that a day with a invalid, suspended game--july 18th 2001--works
        ##### sim_next_day TEST 3

        npsim2001 = NPSimulation(2001, 2001, 15, 16)
        npsim2001.setup()
        npsim2001.set_date(date(2001, 7, 18))
        # artificially inflate bots streaks so that the streak for the bot
        # with player luis gonzalez must get a PASS and stay at 1, and not
        # be able to pass OR reset the streak to stay at zero
        bots = npsim2001.get_bots()
        for bot in bots:
            bot.incr_streak_length()
        for bot in bots: # make sure they all start at 1
            self.assertEqual(bot.get_streak_length(), 1)
        # simulate a day
        npsim2001.sim_next_day()
        
        botPlayers = [
            Player(0, "Ichiro", "Suzuki", 2001), Player(1, "Larry", "Walker", 2001), 
            Player(2, "Jason", "Giambi", 2001), Player(3, "Todd", "Helton", 2001), 
            Player(4, "Roberto", "Alomar", 2001), Player(5, "Moises", "Alou", 2001), 
            Player(6, "Lance", "Berkman", 2001), Player(7, "Bret", "Boone", 2001), 
            Player(8, "Chipper", "Jones", 2001), Player(9, "Frank", "Catalanotto", 2001),
            Player(10, "Albert", "Pujols", 2001), Player(11, "Barry", "Bonds", 2001), 
            Player(12, "Sammy", "Sosa", 2001), Player(13, "Juan", "Pierre", 2001), 
            Player(14, "Luis", "Gonzalez", 2001, debut='9/4/1990')]
        botStreaks = [2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 1]
        bools = map(lambda x: x > 0, botStreaks)
        botDates = [date(2001, 7, 18)] * 15
        HistoriesRaw = zip(zip(botPlayers, bools), zip(botDates, botStreaks))
        botPlayerHistories = [[(f[0], f[1], s[0], s[1], None)] for f, s in HistoriesRaw]
        # bot with luiz gongalez got a 'pass', not a boolean true or false
        botPlayerHistories[-1] = [(
            Player(14, "Luis", "Gonzalez", 2001, debut='9/4/1990'), 
            'pass', date(2001,7,18), 1, "Suspended, Invalid")] 

        self.assertEqual((len(bots)), 15) # check that bots are not empty
        self.assertEqual([bot.get_player() for bot in bots], botPlayers)
        self.assertEqual([bot.get_streak_length() for bot in bots], botStreaks)
        self.assertEqual([bot.get_history() for bot in bots], 
                          botPlayerHistories)
        self.assertEqual(npsim2001.get_date(),date(2001, 7, 19))

    def test_bat_years_ms(self):
        # private function
        sim = NPSimulation(2012, 2012, 50, 50)
        for index, year in enumerate(sim._NPSimulation__bat_years_ms(2012, (0, 3))):
            self.assertTrue(year == (2012, 2011, 2010, 2009)[index])
