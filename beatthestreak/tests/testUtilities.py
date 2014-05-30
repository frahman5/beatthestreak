import unittest
import os
import shutil
import tests

from g import * # get global variables
from data import Data

# @unittest.skip("Focus is not on Utilities right now")
class TestUtilities(unittest.TestCase):

    def setUp(self):
        tests.setup()
        
    def tearDown(self):
        tests.teardown()
    
    def test_convert_date(self):
        self.assertEqual(Utilities.convert_date(date(2012, 4, 15)),"20120415")