import unittest

from tests import setup, teardown
from npsimulation import NPSimulation
from exception import DifficultYearException
from player import Player
from bot import Bot
from datetime import date

# @unittest.skip("Focus is not in Simulation right now")
class TestSimulation(unittest.TestCase):

    npSim2010_1 = NPSimulation(2010, 2010, 100, 35)
    npSim2010_2 = NPSimulation(2010, 2010, 100, 20)
    npSim2001_1 = NPSimulation(2001, 2001, 57, 110)
    npSim2001_2 = NPSimulation(2001, 2001, 57, 19)
    npSim2003_2002 = NPSimulation(2003, 2002, 40, 20)

    players2003_2002 = \
        [Player(0, "Barry", "Bonds", 2002), Player(1, "Manny", "Ramirez", 2002), 
         Player(2, "Mike", "Sweeney", 2002), Player(3, "Larry", "Walker", 2002), 
         Player(4, "Vladimir", "Guerrero", 2002), Player(5, "Bernie", "Williams", 2002, debut='7/7/1991'), 
         Player(6, "Todd", "Helton", 2002),Player(7, "Chipper", "Jones", 2002), 
         Player(8, "Ichiro", "Suzuki", 2002), Player(9, "Magglio", "Ordonez", 2002),
         Player(10, "Jose", "Vidro", 2002), Player(11, "Jason", "Giambi", 2002),
         Player(12, "Albert", "Pujols", 2002), Player(13, "Jeff", "Kent", 2002),
         Player(14, "Adam", "Kennedy", 2002), Player(15, "Jim", "Edmonds", 2002),
         Player(16, "Nomar", "Garciaparra", 2002), Player(17, "Edgardo", "Alfonzo", 2002), 
         Player(18, "Miguel", "Tejada", 2002), Player(19, "Bobby", "Abreu", 2002)] 

    def setUp(self):
        setup()
        
    def tearDown(self):
        teardown()

    # def test_start_date_in_init(self):
    #     npSim2010_1 = NPSimulation(2010, 2010, 100, 35)
    #     self.assertEqual(self.npSim2010_1.get_date(), date(2010, 4, 4))
    #     npSim2010WithStartDate = NPSimulation(2010, 2010, 100, 35, startDate=date(2010,6,7))
    #     self.assertEqual(npSim2010WithStartDate.get_date(),date(2010,6,7))

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
        for index, object in enumerate(bots):
            self.assertEqual(type(object), Bot)
            if index == len(bots)-1:
                break
            self.assertLessEqual(bots[index].get_index(), bots[index+1].get_index())

        ## test that min_bat_ave is calculated and initalized correctly
        self.assertEqual(self.npSim2003_2002.get_min_bat_ave(), 0.308)

    # def test_calc_and_get_min_bat_ave(self): 
    #     self.assertEqual(npSim2010_1.get_min_bat_ave(), 0.290)
    #     self.assertEqual(npSim2010_2.get_min_bat_ave(), 0.300)
    #     self.assertEqual(npSim2001_1.get_min_bat_ave(), 0.266)
    #     self.assertEqual(npSim2001_2.get_min_bat_ave(), 0.319)
    #     self.assertRaises(DifficultYearException, NPSimulation, 1981, 1981, 100, 35)
    #     self.assertRaises(DifficultYearException, NPSimulation, 1950, 1950, 42, 7)

    # def test_get_year(self):
        # self.assertEqual(self.npSim2010_1.get_year(), 2010)
        # self.assertEqual(self.npSim2001_2.get_year(), 2001)

    def test_sim_next_day(self):
        p0, p1, p2, p3, p4, p5, p6, p7, p8, p9 = self.players2003_2002[0:10]
        p10, p11, p12, p13, p14, p15, p16, p17, p18, p19 = self.players2003_2002[10:20]
        bots = self.npSim2003_2002.get_bots()
        
        self.npSim2003_2002.setup() # assume works
        ## check that first day works
        self.npSim2003_2002.sim_next_day()
        # check that bots are not empty
        self.assertEqual(len(bots), 40)
        # check that bots have correct players
        for bot in bots:
            self.assertEqual(bot.get_player(), p13) # p13 is the only ony who played on opening day
        # # check that bots have correct streaks lengths
        # for bot in bots:
        #     self.assertEqual(bot.get_streak_length(), 1) # p13 got a hit on opening day
        # # check that bots have correct player histories
        # for bot in bots:
        #     self.assertEqual([(p13,True)], bot.get_player_history())
        # # check that date on simulation has updated
        # self.assertEqual(self.npSim2003_2002.get_date(), date(2003, 3, 31))

        ## write tests for two other arbitrary days
            # one should account for when there are no games being played


        # check that an arbitrary date works
    # def test_set_n(self):
    #     pass

    # def test_get_n(self):
    #     pass

    # def test_set_p(self):
    #     pass

    # def test_get_p(self):
    #     pass