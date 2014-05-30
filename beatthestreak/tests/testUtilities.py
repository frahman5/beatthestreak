import unittest

from datetime import date
from data import Data
from tests import setup, teardown
from utilities import Utilities

# @unittest.skip("Focus is not on Utilities right now")
class TestUtilities(unittest.TestCase):

    def setUp(self):
        setup()
        
    def tearDown(self):
        teardown()
    
    def test_convert_date(self):
        self.assertEqual(Utilities.convert_date(date(2012, 4, 15)),"20120415")