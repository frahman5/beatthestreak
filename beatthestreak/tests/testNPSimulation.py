import unittest
import os

from datetime import date, timedelta

from beatthestreak.tests import setup, teardown
from beatthestreak.npsimulation import NPSimulation
from beatthestreak.exception import DifficultYearException
from beatthestreak.player import Player
from beatthestreak.bot import Bot
from beatthestreak.filepath import Filepath
from beatthestreak.researcher import Researcher


class TestNPSimulation(unittest.TestCase):

    players2003_2002 = \
        [Player("Barry", "Bonds", 2002), Player("Manny", "Ramirez", 2002), 
         Player("Mike", "Sweeney", 2002), Player("Larry", "Walker", 2002), 
         Player("Vladimir", "Guerrero", 2002), Player("Bernie", "Williams", 2002, debut='7/7/1991'), 
         Player("Todd", "Helton", 2002),Player("Chipper", "Jones", 2002), 
         Player("Ichiro", "Suzuki", 2002), Player("Magglio", "Ordonez", 2002),
         Player("Jose", "Vidro", 2002), Player("Albert", "Pujols", 2002),
         Player("Jason", "Giambi", 2002),Player("Jeff", "Kent", 2002),
         Player("Adam", "Kennedy", 2002), Player("Jim", "Edmonds", 2002),
         Player("Nomar", "Garciaparra", 2002), Player("Bobby", "Abreu", 2002), 
         Player("Miguel", "Tejada", 2002), Player("Edgardo", "Alfonzo", 2002)]

    players_2001_2001_N15_P16 = \
        [Player("Ichiro", "Suzuki", 2001), Player("Larry", "Walker", 2001)  ]
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

    # @unittest.skip("Not Focus")
    def test_start_date_in_init(self):
        self.assertEqual(self.npSim2010_1.get_date(), date(2010, 4, 4))
        self.npSim2010WithStartDate = NPSimulation(
            2010, 2010, 100, 35, startDate=date(2010,6,7))
        self.assertEqual(self.npSim2010WithStartDate.get_date(),date(2010,6,7))

    # @unittest.skip("Too long")
    def test_setup(self):
        self.npSim2003_2002.setup() # sets up the simulation
        self.npSim2003_2002.setup() # to check that repeat setups don't happen

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
        
    @unittest.skip("NEED TO DEBUG OPPOSING_PITCHER_ERA IN YEARS WITH SUS GAMES. ENABLE!!")
    def test_simulate(self):
        ## Single down
            # check that test results folder is empty
        self.assertEqual(os.listdir(Filepath.get_results_folder(
            year=2010, test=True)), [])
            # Run the simulation, shortened to save time
        self.npSim2010_2.simulate(test=True, numDays=10)
        # Check that the results file is now there
        openingDay = Researcher.get_opening_day(2010)
        closingDay = openingDay + timedelta(days=9)
        self.assertTrue(os.path.isfile(Filepath.get_results_file(
            simYear=2010, batAveYear=2010, N=100, P=20, 
            startDate=openingDay, endDate=closingDay, minPA=502, 
            minERA=self.npSim2010_2.minERA, 
            selectionMethodNumber=self.npSim2010_2.method, 
            doubleDown=False, test=True)))

        ## DoubleDOwn
            # check that test results folder is empty
        self.assertEqual(os.listdir(Filepath.get_results_folder(
            year=2009, test=True)), [])
            # Run the simulation, shortened to save time
        npSim = NPSimulation(2009, 2008, 20, 20, doubleDown=True)
        npSim.simulate(test=True, numDays=10)
            # Check that the results file is now there
        openingDay = Researcher.get_opening_day(2009)
        closingDay = openingDay + timedelta(days=9)
        self.assertTrue(os.path.isfile(Filepath.get_results_file(
            simYear=2009, batAveYear=2008, N=20, P=20, 
            startDate=openingDay, endDate=closingDay, 
            minPA=502, minERA=self.npSim2010_2.minERA, 
            selectionMethodNumber=self.npSim2010_2.method, 
            doubleDown=True, test=True)))

    @unittest.skip("Not Yet")
    def test_mass_simulate(self):
        # just checks that it runs
        self.npSim2001_1.mass_simulate((2001, 2002), (1, 3), (1, 5), (1, 5), 
            test=True)

    # @unittest.skip("Not Focus")
    def test_get_year(self):
        self.assertEqual(self.npSim2010_1.get_sim_year(), 2010)
        self.assertEqual(self.npSim2001_2.get_sim_year(), 2001)

    # @unittest.skip("Not focus")
    def test_sim_next_day_without_double_down(self):
        p0, p1, p2, p3, p4, p5, p6, p7, p8, p9 = self.players2003_2002[0:10]
        p10, p11, p12, p13, p14, p15, p16, p17, p18, p19 = self.players2003_2002[10:20]

        self.npSim2003_2002.setup() # assume works
        bots = self.npSim2003_2002.get_bots()

        ####### check that first day works (TEST 1)
        self.npSim2003_2002.sim_next_day()
        self.assertEqual(len(bots), 40) # check that bots are not empty
        self.assertEqual([bot.get_players() for bot in bots], [(p14,None)] * 40)
        self.assertEqual([bot.get_streak_length() for bot in bots], [1] * 40)
        self.assertEqual([bot.get_history() for bot in bots], 
            [[(p14, None, True, None, date(2003, 3, 30), 1, None)]] * 40)
        self.assertEqual(self.npSim2003_2002.get_date(), date(2003, 3, 31))
        
        ######## check that an arbitrary day-May 14-works (TEST 2)
        self.npSim2003_2002.set_date(date(2003, 5, 14))
        self.npSim2003_2002.sim_next_day()

        botPlayersRaw = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, 
                      p11, p12, p13, p15, p16, p17, p18, p19, p0, p1, 
                      p2, p3, p4, p5, p6, p7, p8, p9, p11, p12, 
                      p13, p15, p16, p17, p18, p19, p0, p1, p2, p3]
        botPlayers = [(player, None) for player in botPlayersRaw]
        botStreaks = [2,0,2,2,2,2,0,0,2,0, 
                      0,0,2,0,2,2,2,2,2,0,
                      2,2,2,2,0,0,2,0,0,0,
                      2,0,2,2,2,2,2,0,2,2]
        bools = map(lambda x: x > 0, botStreaks)
        botDates = [date(2003, 5, 14)] * 40

        day2resultsRaw = zip(zip(botPlayers, bools), zip(botDates, botStreaks))
        day2results = [(f[0][0], f[0][1], f[1], None, s[0], s[1], None) 
            for f, s in day2resultsRaw]
        botPlayerHistories = [
            [(p14, None, True, None, date(2003, 3, 30), 1, None), day2] for \
              day2 in day2results]
             
        self.assertEqual(len(bots), 40) # check that bots are not empty
        self.assertEqual([bot.get_players() for bot in bots], botPlayers)
        self.assertEqual([bot.get_streak_length() for bot in bots], botStreaks)
        self.assertEqual([bot.get_history() for bot in bots], 
                         botPlayerHistories)
        self.assertEqual(self.npSim2003_2002.get_date(), date(2003, 5, 15))
        self.__sim_next_day_t_3_without_double_down()

    def __sim_next_day_t_3_without_double_down(self):
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
        
        botPlayersRaw = [
            Player("Ichiro", "Suzuki", 2001), Player("Larry", "Walker", 2001), 
            Player("Jason", "Giambi", 2001), Player("Todd", "Helton", 2001), 
            Player("Roberto", "Alomar", 2001), Player("Moises", "Alou", 2001), 
            Player("Lance", "Berkman", 2001), Player("Bret", "Boone", 2001), 
            Player("Chipper", "Jones", 2001), Player("Frank", "Catalanotto", 2001),
            Player("Albert", "Pujols", 2001), Player("Barry", "Bonds", 2001), 
            Player("Sammy", "Sosa", 2001), Player("Juan", "Pierre", 2001), 
            Player("Luis", "Gonzalez", 2001, debut='9/4/1990')]
        botPlayers = [(player, None) for player in botPlayersRaw]
        botStreaks = [2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 1]
        bools = map(lambda x: x > 0, botStreaks)
        botDates = [date(2001, 7, 18)] * 15
        HistoriesRaw = zip(zip(botPlayers, bools), zip(botDates, botStreaks))
        botPlayerHistories = [[(f[0][0], f[0][1], f[1], None, s[0], s[1], None)] 
            for f, s in HistoriesRaw]
        # bot with luiz gongalez got a 'pass', not a boolean true or false
        botPlayerHistories[-1] = [(
            Player("Luis", "Gonzalez", 2001, debut='9/4/1990'), None,
            'pass', None, date(2001,7,18), 1, "Suspended-Invalid.")] 

        self.assertEqual((len(bots)), 15) # check that bots are not empty
        self.assertEqual([bot.get_players() for bot in bots], botPlayers)
        self.assertEqual([bot.get_streak_length() for bot in bots], botStreaks)
        self.assertEqual([bot.get_history() for bot in bots], 
                          botPlayerHistories)
        self.assertEqual(npsim2001.get_date(),date(2001, 7, 19))

    # @unittest.skip("Not focus")
    def test_sim_next_day_with_double_down(self):
        p0, p1, p2, p3, p4, p5, p6, p7, p8, p9 = self.players2003_2002[0:10]
        p10, p11, p12, p13, p14, p15, p16, p17, p18, p19 = self.players2003_2002[10:20]

        self.npSim2003_2002.setup() # assume works
        bots = self.npSim2003_2002.get_bots()

        ####### check that first day works (TEST 1)
        self.npSim2003_2002.sim_next_day(doubleDown=True)
        self.assertEqual(len(bots), 40) # check that bots are not empty
            # If only one player is active on a given date, then bots 
            # should end up NOT doubling down
        self.assertEqual([bot.get_players() for bot in bots], [(p14,None)] * 40)
        self.assertEqual([bot.get_streak_length() for bot in bots], [1] * 40)
        self.assertEqual([bot.get_history() for bot in bots], 
            [[(p14, None, True, None, date(2003, 3, 30), 1, None)]] * 40)
        self.assertEqual(self.npSim2003_2002.get_date(), date(2003, 3, 31))
        
        ######## check that an arbitrary day-May 14-works (TEST 2)
            # set date and simulate
        self.npSim2003_2002.set_date(date(2003, 5, 14))
        self.npSim2003_2002.sim_next_day(doubleDown=True)
            # write down correct answers
        botPlayers = [
            (p0, p1), (p2, p3), (p4, p5), (p6, p7), (p8, p9), (p11, p12), 
            (p13, p15), (p16, p17), (p18, p19), (p0, p1), (p2, p3), (p4, p5), 
            (p6, p7), (p8, p9), (p11, p12), (p13, p15), (p16, p17), (p18, p19), 
            (p0, p1), (p2, p3), (p4, p5), (p6, p7), (p8, p9), (p11, p12), 
            (p13, p15), (p16, p17), (p18, p19), (p0, p1), (p2, p3), (p4, p5), 
            (p6, p7), (p8, p9), (p11, p12), (p13, p15), (p16, p17), (p18, p19), 
            (p0, p1), (p2, p3), (p4, p5), (p6, p7)]
        botStreaks = [
                    0, 3, 3, 0, 0, 0, 0, 3, 3, 
                    0, 3, 3, 0, 0, 0, 0, 3, 3, 
                    0, 3, 3, 0, 0, 0, 0, 3, 3, 
                    0, 3, 3, 0, 0, 0, 0, 3, 3, 
                    0, 3, 3, 0]
        bools = [
            (True, False), (True, True), (True, True), (False, False), 
            (True, False), (False, False), (True, False), (True, True), 
            (True, True), (True, False), (True, True), (True, True), 
            (False, False), (True, False), (False, False), (True, False), 
            (True, True), (True, True), (True, False), (True, True), 
            (True, True), (False, False), (True, False), (False, False), 
            (True, False), (True, True), (True, True), (True, False), 
            (True, True), (True, True), (False, False), (True, False), 
            (False, False), (True, False), (True, True), (True, True), 
            (True, False), (True, True), (True, True), (False, False)]
        botDates = [date(2003, 5, 14)] * 40
        day2resultsRaw = zip(zip(botPlayers, bools), zip(botDates, botStreaks))
        day2results = [(f[0][0], f[0][1], f[1][0], f[1][1], s[0], s[1], None) 
            for f, s in day2resultsRaw]
        botPlayerHistories = [
            [(p14, None, True, None, date(2003, 3, 30), 1, None), day2] for \
              day2 in day2results]
        
        self.assertEqual(len(bots), 40) # check that bots are not empty
        self.assertEqual([bot.get_players() for bot in bots], botPlayers)
        self.assertEqual([bot.get_streak_length() for bot in bots], botStreaks)
        self.assertEqual([bot.get_history() for bot in bots], 
                         botPlayerHistories)
        self.assertEqual(self.npSim2003_2002.get_date(), date(2003, 5, 15))

    # @unittest.skip("Not focus")
    def test_bat_years_ms(self):
        # private function
        sim = NPSimulation(2012, 2012, 50, 50)
        for index, year in enumerate(sim._NPSimulation__bat_years_ms(2012, (0, 3))):
            self.assertTrue(year == (2009, 2010, 2011, 2012)[index])
    def test__get_min_pa_range(self):
        # private function
        sim = NPSimulation(2012, 2012, 50, 50)

        ## Case 1: Upper bound is < lower bound + 100
        g = sim._NPSimulation__get_min_pa_range(5, 104)
        self.assertEqual( set(g), set([5,104]))

        ## Case 2: Upper bound is > lower bound, not exactly a multiple of 100 away
        g = sim._NPSimulation__get_min_pa_range(100, 201)
        self.assertEqual( set(g), set([100, 200, 201]))

        ## case 3: Upper bound is > lower bound, exactly a multiple of 100 away
        g = sim._NPSimulation__get_min_pa_range(104, 304)
        self.assertEqual( set(g), set([104, 204, 304]))

        ## Case 4: Upper bound = lower bound
        self.assertEqual( set(sim._NPSimulation__get_min_era_range(200, 200)), 
                          set([200]))

    def test___get_min_era_range(self):
        # private function
        sim = NPSimulation(2010, 2009, 10, 10)

        ## Case 1: Upper bound is < lower bound + 0.5
        g = sim._NPSimulation__get_min_era_range(2.0, 2.4)
        self.assertEqual( set(g), set([2.0, 2.4]))

        ## Case 2: Upper bound is > lowerbound + 0.5, but not exactly a multiple of 0.5 away
        g = sim._NPSimulation__get_min_era_range(2.0, 5.4)
        self.assertEqual( set(g), set([2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.4]))

        ## Case 3: Upper bound is > lowerbound, exactly a multiple of 0.5 away
        g = sim._NPSimulation__get_min_era_range(1.0, 3.5)
        self.assertEqual( set(g), set([1.0, 1.5, 2.0, 2.5, 3.0, 3.5]))

        ## Case 4: Upper bound = lowerbound
        self.assertEqual( set(sim._NPSimulation__get_min_era_range(5.7, 5.7)), 
                          set([5.7]))

    def test__create_mass_sim_param_generator(self):
        # priate function
        sim = NPSimulation(2012, 2012, 50, 50)

        ## Case 1: method in (1,2)
        params, paramsLength = sim._NPSimulation__create_mass_sim_param_generator(
                                    (2010, 2011), (1, 2), (100, 102), 
                                    (20, 21), (100, 200))
        self.assertEqual(paramsLength, 64)
        self.assertEqual(set(params), 
            set([ (2010, 2009, 100, 20, 100, True), 
                  (2010, 2009, 100, 20, 200, True), 
                  (2010, 2009, 100, 21, 100, True), 
                  (2010, 2009, 100, 21, 200, True), 
                  (2010, 2009, 102, 20, 100, True), 
                  (2010, 2009, 102, 20, 200, True), 
                  (2010, 2009, 102, 21, 100, True), 
                  (2010, 2009, 102, 21, 200, True), 
                  (2010, 2008, 100, 20, 100, True), 
                  (2010, 2008, 100, 20, 200, True), 
                  (2010, 2008, 100, 21, 100, True), 
                  (2010, 2008, 100, 21, 200, True), 
                  (2010, 2008, 102, 20, 100, True), 
                  (2010, 2008, 102, 20, 200, True), 
                  (2010, 2008, 102, 21, 100, True), 
                  (2010, 2008, 102, 21, 200, True), 

                  (2010, 2009, 100, 20, 100, False), 
                  (2010, 2009, 100, 20, 200, False), 
                  (2010, 2009, 100, 21, 100, False), 
                  (2010, 2009, 100, 21, 200, False),  
                  (2010, 2009, 102, 20, 100, False), 
                  (2010, 2009, 102, 20, 200, False), 
                  (2010, 2009, 102, 21, 100, False), 
                  (2010, 2009, 102, 21, 200, False), 
                  (2010, 2008, 100, 20, 100, False), 
                  (2010, 2008, 100, 20, 200, False), 
                  (2010, 2008, 100, 21, 100, False), 
                  (2010, 2008, 100, 21, 200, False), 
                  (2010, 2008, 102, 20, 100, False), 
                  (2010, 2008, 102, 20, 200, False), 
                  (2010, 2008, 102, 21, 100, False), 
                  (2010, 2008, 102, 21, 200, False), 

                  (2011, 2010, 100, 20, 100, True), 
                  (2011, 2010, 100, 20, 200, True), 
                  (2011, 2010, 100, 21, 100, True), 
                  (2011, 2010, 100, 21, 200, True), 
                  (2011, 2010, 102, 20, 100, True), 
                  (2011, 2010, 102, 20, 200, True), 
                  (2011, 2010, 102, 21, 100, True), 
                  (2011, 2010, 102, 21, 200, True), 
                  (2011, 2009, 100, 20, 100, True), 
                  (2011, 2009, 100, 20, 200, True), 
                  (2011, 2009, 100, 21, 100, True), 
                  (2011, 2009, 100, 21, 200, True), 
                  (2011, 2009, 102, 20, 100, True), 
                  (2011, 2009, 102, 20, 200, True), 
                  (2011, 2009, 102, 21, 100, True), 
                  (2011, 2009, 102, 21, 200, True), 

                  (2011, 2010, 100, 20, 100, False), 
                  (2011, 2010, 100, 20, 200, False), 
                  (2011, 2010, 100, 21, 100, False), 
                  (2011, 2010, 100, 21, 200, False),  
                  (2011, 2010, 102, 20, 100, False), 
                  (2011, 2010, 102, 20, 200, False), 
                  (2011, 2010, 102, 21, 100, False), 
                  (2011, 2010, 102, 21, 200, False), 
                  (2011, 2009, 100, 20, 100, False), 
                  (2011, 2009, 100, 20, 200, False), 
                  (2011, 2009, 100, 21, 100, False), 
                  (2011, 2009, 100, 21, 200, False), 
                  (2011, 2009, 102, 20, 100, False), 
                  (2011, 2009, 102, 20, 200, False), 
                  (2011, 2009, 102, 21, 100, False), 
                  (2011, 2009, 102, 21, 200, False) ]))
        
        params, paramsLength = sim._NPSimulation__create_mass_sim_param_generator(
                                    (2010, 2011), (1, 2), (100, 101), 
                                    (20, 21), (100, 200), (1.0, 2.0), method=3)
        self.assertEqual(paramsLength, 192)
        self.assertEqual(set(params),
            set([
                (2010, 2009, 100, 20, 100, 1.0, True),
                (2010, 2009, 100, 20, 100, 1.5, True),
                (2010, 2009, 100, 20, 100, 2.0, True),
                (2010, 2009, 100, 20, 200, 1.0, True),
                (2010, 2009, 100, 20, 200, 1.5, True),
                (2010, 2009, 100, 20, 200, 2.0, True),
                (2010, 2009, 100, 21, 100, 1.0, True),
                (2010, 2009, 100, 21, 100, 1.5, True),
                (2010, 2009, 100, 21, 100, 2.0, True),
                (2010, 2009, 100, 21, 200, 1.0, True),
                (2010, 2009, 100, 21, 200, 1.5, True),
                (2010, 2009, 100, 21, 200, 2.0, True),
                (2010, 2009, 101, 20, 100, 1.0, True),
                (2010, 2009, 101, 20, 100, 1.5, True),
                (2010, 2009, 101, 20, 100, 2.0, True),
                (2010, 2009, 101, 20, 200, 1.0, True),
                (2010, 2009, 101, 20, 200, 1.5, True),
                (2010, 2009, 101, 20, 200, 2.0, True),
                (2010, 2009, 101, 21, 100, 1.0, True),
                (2010, 2009, 101, 21, 100, 1.5, True),
                (2010, 2009, 101, 21, 100, 2.0, True),
                (2010, 2009, 101, 21, 200, 1.0, True),
                (2010, 2009, 101, 21, 200, 1.5, True),
                (2010, 2009, 101, 21, 200, 2.0, True),
                (2010, 2008, 100, 20, 100, 1.0, True),
                (2010, 2008, 100, 20, 100, 1.5, True),
                (2010, 2008, 100, 20, 100, 2.0, True),
                (2010, 2008, 100, 20, 200, 1.0, True),
                (2010, 2008, 100, 20, 200, 1.5, True),
                (2010, 2008, 100, 20, 200, 2.0, True),
                (2010, 2008, 100, 21, 100, 1.0, True),
                (2010, 2008, 100, 21, 100, 1.5, True),
                (2010, 2008, 100, 21, 100, 2.0, True),
                (2010, 2008, 100, 21, 200, 1.0, True),
                (2010, 2008, 100, 21, 200, 1.5, True),
                (2010, 2008, 100, 21, 200, 2.0, True),
                (2010, 2008, 101, 20, 100, 1.0, True),
                (2010, 2008, 101, 20, 100, 1.5, True),
                (2010, 2008, 101, 20, 100, 2.0, True),
                (2010, 2008, 101, 20, 200, 1.0, True),
                (2010, 2008, 101, 20, 200, 1.5, True),
                (2010, 2008, 101, 20, 200, 2.0, True),
                (2010, 2008, 101, 21, 100, 1.0, True),
                (2010, 2008, 101, 21, 100, 1.5, True),
                (2010, 2008, 101, 21, 100, 2.0, True),
                (2010, 2008, 101, 21, 200, 1.0, True),
                (2010, 2008, 101, 21, 200, 1.5, True),
                (2010, 2008, 101, 21, 200, 2.0, True),

                (2011, 2010, 100, 20, 100, 1.0, True),
                (2011, 2010, 100, 20, 100, 1.5, True),
                (2011, 2010, 100, 20, 100, 2.0, True),
                (2011, 2010, 100, 20, 200, 1.0, True),
                (2011, 2010, 100, 20, 200, 1.5, True),
                (2011, 2010, 100, 20, 200, 2.0, True),
                (2011, 2010, 100, 21, 100, 1.0, True),
                (2011, 2010, 100, 21, 100, 1.5, True),
                (2011, 2010, 100, 21, 100, 2.0, True),
                (2011, 2010, 100, 21, 200, 1.0, True),
                (2011, 2010, 100, 21, 200, 1.5, True),
                (2011, 2010, 100, 21, 200, 2.0, True),
                (2011, 2010, 101, 20, 100, 1.0, True),
                (2011, 2010, 101, 20, 100, 1.5, True),
                (2011, 2010, 101, 20, 100, 2.0, True),
                (2011, 2010, 101, 20, 200, 1.0, True),
                (2011, 2010, 101, 20, 200, 1.5, True),
                (2011, 2010, 101, 20, 200, 2.0, True),
                (2011, 2010, 101, 21, 100, 1.0, True),
                (2011, 2010, 101, 21, 100, 1.5, True),
                (2011, 2010, 101, 21, 100, 2.0, True),
                (2011, 2010, 101, 21, 200, 1.0, True),
                (2011, 2010, 101, 21, 200, 1.5, True),
                (2011, 2010, 101, 21, 200, 2.0, True),
                (2011, 2009, 100, 20, 100, 1.0, True),
                (2011, 2009, 100, 20, 100, 1.5, True),
                (2011, 2009, 100, 20, 100, 2.0, True),
                (2011, 2009, 100, 20, 200, 1.0, True),
                (2011, 2009, 100, 20, 200, 1.5, True),
                (2011, 2009, 100, 20, 200, 2.0, True),
                (2011, 2009, 100, 21, 100, 1.0, True),
                (2011, 2009, 100, 21, 100, 1.5, True),
                (2011, 2009, 100, 21, 100, 2.0, True),
                (2011, 2009, 100, 21, 200, 1.0, True),
                (2011, 2009, 100, 21, 200, 1.5, True),
                (2011, 2009, 100, 21, 200, 2.0, True),
                (2011, 2009, 101, 20, 100, 1.0, True),
                (2011, 2009, 101, 20, 100, 1.5, True),
                (2011, 2009, 101, 20, 100, 2.0, True),
                (2011, 2009, 101, 20, 200, 1.0, True),
                (2011, 2009, 101, 20, 200, 1.5, True),
                (2011, 2009, 101, 20, 200, 2.0, True),
                (2011, 2009, 101, 21, 100, 1.0, True),
                (2011, 2009, 101, 21, 100, 1.5, True),
                (2011, 2009, 101, 21, 100, 2.0, True),
                (2011, 2009, 101, 21, 200, 1.0, True),
                (2011, 2009, 101, 21, 200, 1.5, True), 
                (2011, 2009, 101, 21, 200, 2.0, True), 

                (2010, 2009, 100, 20, 100, 1.0, False),
                (2010, 2009, 100, 20, 100, 1.5, False),
                (2010, 2009, 100, 20, 100, 2.0, False),
                (2010, 2009, 100, 20, 200, 1.0, False),
                (2010, 2009, 100, 20, 200, 1.5, False),
                (2010, 2009, 100, 20, 200, 2.0, False),
                (2010, 2009, 100, 21, 100, 1.0, False),
                (2010, 2009, 100, 21, 100, 1.5, False),
                (2010, 2009, 100, 21, 100, 2.0, False),
                (2010, 2009, 100, 21, 200, 1.0, False),
                (2010, 2009, 100, 21, 200, 1.5, False),
                (2010, 2009, 100, 21, 200, 2.0, False),
                (2010, 2009, 101, 20, 100, 1.0, False),
                (2010, 2009, 101, 20, 100, 1.5, False),
                (2010, 2009, 101, 20, 100, 2.0, False),
                (2010, 2009, 101, 20, 200, 1.0, False),
                (2010, 2009, 101, 20, 200, 1.5, False),
                (2010, 2009, 101, 20, 200, 2.0, False),
                (2010, 2009, 101, 21, 100, 1.0, False),
                (2010, 2009, 101, 21, 100, 1.5, False),
                (2010, 2009, 101, 21, 100, 2.0, False),
                (2010, 2009, 101, 21, 200, 1.0, False),
                (2010, 2009, 101, 21, 200, 1.5, False),
                (2010, 2009, 101, 21, 200, 2.0, False),
                (2010, 2008, 100, 20, 100, 1.0, False),
                (2010, 2008, 100, 20, 100, 1.5, False),
                (2010, 2008, 100, 20, 100, 2.0, False),
                (2010, 2008, 100, 20, 200, 1.0, False),
                (2010, 2008, 100, 20, 200, 1.5, False),
                (2010, 2008, 100, 20, 200, 2.0, False),
                (2010, 2008, 100, 21, 100, 1.0, False),
                (2010, 2008, 100, 21, 100, 1.5, False),
                (2010, 2008, 100, 21, 100, 2.0, False),
                (2010, 2008, 100, 21, 200, 1.0, False),
                (2010, 2008, 100, 21, 200, 1.5, False),
                (2010, 2008, 100, 21, 200, 2.0, False),
                (2010, 2008, 101, 20, 100, 1.0, False),
                (2010, 2008, 101, 20, 100, 1.5, False),
                (2010, 2008, 101, 20, 100, 2.0, False),
                (2010, 2008, 101, 20, 200, 1.0, False),
                (2010, 2008, 101, 20, 200, 1.5, False),
                (2010, 2008, 101, 20, 200, 2.0, False),
                (2010, 2008, 101, 21, 100, 1.0, False),
                (2010, 2008, 101, 21, 100, 1.5, False),
                (2010, 2008, 101, 21, 100, 2.0, False),
                (2010, 2008, 101, 21, 200, 1.0, False),
                (2010, 2008, 101, 21, 200, 1.5, False),
                (2010, 2008, 101, 21, 200, 2.0, False),

                (2011, 2010, 100, 20, 100, 1.0, False),
                (2011, 2010, 100, 20, 100, 1.5, False),
                (2011, 2010, 100, 20, 100, 2.0, False),
                (2011, 2010, 100, 20, 200, 1.0, False),
                (2011, 2010, 100, 20, 200, 1.5, False),
                (2011, 2010, 100, 20, 200, 2.0, False),
                (2011, 2010, 100, 21, 100, 1.0, False),
                (2011, 2010, 100, 21, 100, 1.5, False),
                (2011, 2010, 100, 21, 100, 2.0, False),
                (2011, 2010, 100, 21, 200, 1.0, False),
                (2011, 2010, 100, 21, 200, 1.5, False),
                (2011, 2010, 100, 21, 200, 2.0, False),
                (2011, 2010, 101, 20, 100, 1.0, False),
                (2011, 2010, 101, 20, 100, 1.5, False),
                (2011, 2010, 101, 20, 100, 2.0, False),
                (2011, 2010, 101, 20, 200, 1.0, False),
                (2011, 2010, 101, 20, 200, 1.5, False),
                (2011, 2010, 101, 20, 200, 2.0, False),
                (2011, 2010, 101, 21, 100, 1.0, False),
                (2011, 2010, 101, 21, 100, 1.5, False),
                (2011, 2010, 101, 21, 100, 2.0, False),
                (2011, 2010, 101, 21, 200, 1.0, False),
                (2011, 2010, 101, 21, 200, 1.5, False),
                (2011, 2010, 101, 21, 200, 2.0, False),
                (2011, 2009, 100, 20, 100, 1.0, False),
                (2011, 2009, 100, 20, 100, 1.5, False),
                (2011, 2009, 100, 20, 100, 2.0, False),
                (2011, 2009, 100, 20, 200, 1.0, False),
                (2011, 2009, 100, 20, 200, 1.5, False),
                (2011, 2009, 100, 20, 200, 2.0, False),
                (2011, 2009, 100, 21, 100, 1.0, False),
                (2011, 2009, 100, 21, 100, 1.5, False),
                (2011, 2009, 100, 21, 100, 2.0, False),
                (2011, 2009, 100, 21, 200, 1.0, False),
                (2011, 2009, 100, 21, 200, 1.5, False),
                (2011, 2009, 100, 21, 200, 2.0, False),
                (2011, 2009, 101, 20, 100, 1.0, False),
                (2011, 2009, 101, 20, 100, 1.5, False),
                (2011, 2009, 101, 20, 100, 2.0, False),
                (2011, 2009, 101, 20, 200, 1.0, False),
                (2011, 2009, 101, 20, 200, 1.5, False),
                (2011, 2009, 101, 20, 200, 2.0, False),
                (2011, 2009, 101, 21, 100, 1.0, False),
                (2011, 2009, 101, 21, 100, 1.5, False),
                (2011, 2009, 101, 21, 100, 2.0, False),
                (2011, 2009, 101, 21, 200, 1.0, False),
                (2011, 2009, 101, 21, 200, 1.5, False), 
                (2011, 2009, 101, 21, 200, 2.0, False) ]))
        
