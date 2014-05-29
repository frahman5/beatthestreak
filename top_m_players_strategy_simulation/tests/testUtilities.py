import unittest

from g import * # get global variables

class TestUtilities(unittest.TestCase):
    
    def test_convert_date(self):
        self.assertEqual(Utilities.convert_date(date(2012, 4, 15)),"20120415")