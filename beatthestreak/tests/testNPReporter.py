import unittest

from datetime import date

from beatthestreak.npreporter import NPReporter 
from beatthestreak.player import Player
from beatthestreak.npsimulation import NPSimulation
from beatthestreak.researcher import Researcher

from beatthestreak.tests import setup, teardown

class testNPReporter(unittest.TestCase):

    def setUp(self):
    	setup()

    def tearDown(self):
    	teardown()

    def test__calc_unique_bots(self):
	    sim = NPSimulation(2012, 2012, 50, 50)
	    reporter = NPReporter(sim)
	    sGD2012 = Researcher.get_sus_games_dict(2012)

	    sim.bots = sim._create_bots() # make 50 bots, should only be 1 "unique" bot
	    self.assertEqual(reporter._NPReporter__calc_num_unique_bots(), 1)

	    # change one bot so that its different
	    sim.get_bots()[4].update_history(
	        p1=Player("Manny", "Ramirez", 2010), date=date(2009, 9, 9), 
	        susGamesDict=sGD2012)
	    # should now be 2 "unique" bots
	    self.assertEqual(reporter._NPReporter__calc_num_unique_bots(), 2)