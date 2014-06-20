import unittest
from datetime import date
from beatthestreak.tests import p1, p2, p3, p4, p5

from cresearcher import did_get_hit

class TestCResearcher(unittest.TestCase):

    def test_did_get_hit(self):
        self.assertFalse(did_get_hit())
        # # Edwin Jackon test
        # self.assertFalse(did_get_hit(date(2012, 5, 2), p1))

        # # Jose Reyes Tests (and one Albert Pujols)
        # self.assertTrue(did_get_hit(date(2012, 6, 16), p2))
        # self.assertTrue(did_get_hit(date(2005, 4, 4), p2))
        # self.assertTrue(did_get_hit(date(2003, 7, 12), p2))
        # self.assertFalse(did_get_hit(date(2012, 6, 15), p2))
        # self.assertFalse(did_get_hit(date(2008, 9, 21), p2))

        # # Alfonso Soriano Tests
        # self.assertTrue(did_get_hit(date(2003, 3, 31), p3))
        # self.assertTrue(did_get_hit(date(2009, 5, 12), p3))
        # self.assertFalse(did_get_hit(date(2001, 9, 4), p3))
        # self.assertFalse(did_get_hit(date(2007, 7, 20), p3))
        # self.assertFalse(did_get_hit(date(2004, 9, 16), p3))

        # # Jorge Posada tests
        # self.assertTrue(did_get_hit(date(2004, 8, 17), p4))
        # self.assertTrue(did_get_hit(date(2010, 7, 11), p4))
        # self.assertFalse(did_get_hit(date(1997, 5, 23), p4))
        # self.assertFalse(did_get_hit(date(2000, 4, 30), p4))

        # # Manny Ramirez tests (traded in 2008. This test checks to see
        # #   if did_get_hit works for players in a year they are traded)
        # self.assertTrue(did_get_hit(date(1994, 7, 26), p5))
        # self.assertTrue(did_get_hit(date(2008, 5, 22), p5))
        # self.assertTrue(did_get_hit(date(2008, 8, 1), p5))
        # self.assertFalse(did_get_hit(date(1995, 6, 30), p5))
        # self.assertFalse(did_get_hit(date(2008, 7, 29), p5))
        # self.assertFalse(did_get_hit(date(2008, 8, 31), p5))

        # ## Larry Jones, from Player, test. Tests to see if it works even if
        # ## the player has a nickname (Goes by Chipper instead of Larry)
        # pL = Player('jonesch06', 2003)
        # self.assertTrue(did_get_hit(date(2003, 4, 19), pL))
        # self.assertFalse(did_get_hit(date(2003, 8, 28), pL))

        # # Test Miguel Cabrera, Asdrubal Cabrera, Delmon Young, Michael Young.
        # # Checks for proper answer when the functional line of the boxscore
        # # has two players with the same last name
        # MC1 = Player("Miguel", "Cabrera", 2012)
        # MC2 = Player("Asdrubal", "Cabrera", 2012)
        # dateMC = date(2012, 9, 5)
        # self.assertTrue(did_get_hit(dateMC, MC1))
        # self.assertFalse(did_get_hit(dateMC, MC2))

        # MY1 = Player("Michael", "Young", 2012)
        # MY2 = Player("Delmon", "Young", 2012)
        # dateMY = date(2012, 6, 26)
        # self.assertTrue(did_get_hit(dateMY, MY1))
        # self.assertFalse(did_get_hit(dateMY, MY2))

        # ## Double Header tests (its a hit iff player got a hit in first game)
        # self.assertFalse(did_get_hit(date(1996, 9, 25), p4)) # T1, H2
        # self.assertFalse(did_get_hit(date(2008, 9, 7), p2)) # T1, T2
        # self.assertTrue(did_get_hit(date(2007, 7, 28), p2)) # H1, T2
        # self.assertTrue(did_get_hit(date(2006, 6, 3), p2)) # H1, H2

        # # Lance Berkman tests
        # Lance = Player("Lance", "Berkman", 2008)
        # self.assertTrue(did_get_hit(date(2009, 7, 9), Lance))