import unittest
import os
import shutil

from data import Data
from simulation import Simulation
from tests import setup, teardown
from npsimulation import NPSimulation
from exception import DifficultYearException

npSim2010_1 = NPSimulation(2010, 2010, 100, 35)
npSim2010_2 = NPSimulation(2010, 2010, 100, 20)
npSim2001_1 = NPSimulation(2001, 2001, 57, 110)
npSim2001_2 = NPSimulation(2001, 2001, 57, 19)

# @unittest.skip("Focus is not in Simulation right now")
class TestSimulation(unittest.TestCase):

    def setUp(self):
        setup()
        
    def tearDown(self):
        teardown()

    def test_set_and_get_min_bat_ave(self): 
        self.assertEqual(npSim2010_1.get_min_bat_ave(), 0.290)
        self.assertEqual(npSim2010_2.get_min_bat_ave(), 0.300)
        self.assertEqual(npSim2001_1.get_min_bat_ave(), 0.266)
        self.assertEqual(npSim2001_2.get_min_bat_ave(), 0.319)
        self.assertRaises(DifficultYearException, NPSimulation, 1981, 1981, 100, 35)
        self.assertRaises(DifficultYearException, NPSimulation, 1950, 1950, 42, 7)

    def test_get_year(self):
        # self.assertEqual(npSim2010_1.get_year(), 2010)
        self.assertEqual(npSim2001_2.get_year(), 2001)

    def test_set_n(self):
        pass

    def test_get_n(self):
        pass

    def test_set_p(self):
        pass

    def test_get_p(self):
        pass
