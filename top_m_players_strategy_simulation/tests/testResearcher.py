import unittest

from g import *
class TestSimulation(unittest.TestCase):
    
    def test_get_participants(self):
    	self.assertEqual(r1.get_participants(date(2011,9,4)), 
        	             participants_2011_9_4)
        self.assertEqual(r1.get_participants(date(2012,3,28)), 
        	             participants_2012_3_28)
        self.assertEqual(r1.get_participants(date(2013,6,7)), 
        	             participants_2013_6_7)