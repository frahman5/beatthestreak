import unittest

from datetime import date

from beatthestreak.npreporter import NPReporter 
from beatthestreak.player import Player
from beatthestreak.npsimulation import NPSimulation

from beatthestreak.tests import setup, teardown

class testNPReporter(unittest.TestCase):

    def setUp(self):
    	setup()

    def tearDown(self):
    	teardown()

    def test__calc_unique_bots(self):
	    sim = NPSimulation(2012, 2012, 50, 50)
	    reporter = NPReporter(sim)

	    sim.bots = sim._create_bots()
	    self.assertEqual(reporter._NPReporter__calc_num_unique_bots(), 1)
	    sim.get_bots()[4].update_history(
	        Player(0, "Manny", "Ramirez", 2010), True, date(2012, 9, 9))
	    self.assertEqual(reporter._NPReporter__calc_num_unique_bots(), 2)