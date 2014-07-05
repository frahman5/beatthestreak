import unittest
from datetime import date
from beatthestreak.tests import p1, p2, p3, p4, p5

from beatthestreak.researcher import Researcher as R
from beatthestreak.player import Player
from beatthestreak.filepath import Filepath
from cresearcher import cfinish_did_get_hit, cget_hit_info, cdid_start, copposing_pitcher_era

class TestCResearcher(unittest.TestCase):

    def test_c_did_get_hit(self):
        # Edwin Jackon test
        self.assertFalse(R.c_did_get_hit(date(2012, 5, 2), p1))

        # # Jose Reyes Tests (and one Albert Pujols)
        self.assertTrue(R.c_did_get_hit(date(2012, 6, 16), p2))
        self.assertTrue(R.c_did_get_hit(date(2005, 4, 4), p2))
        self.assertTrue(R.c_did_get_hit(date(2003, 7, 12), p2))
        self.assertFalse(R.c_did_get_hit(date(2012, 6, 15), p2))
        self.assertFalse(R.c_did_get_hit(date(2008, 9, 21), p2))

        # Alfonso Soriano Tests
        self.assertTrue(R.c_did_get_hit(date(2003, 3, 31), p3))
        self.assertTrue(R.c_did_get_hit(date(2009, 5, 12), p3))
        self.assertFalse(R.c_did_get_hit(date(2001, 9, 4), p3))
        self.assertFalse(R.c_did_get_hit(date(2007, 7, 20), p3))
        self.assertFalse(R.c_did_get_hit(date(2004, 9, 16), p3))

        # Jorge Posada tests
        self.assertTrue(R.c_did_get_hit(date(2004, 8, 17), p4))
        self.assertTrue(R.c_did_get_hit(date(2010, 7, 11), p4))
        self.assertFalse(R.c_did_get_hit(date(1997, 5, 23), p4))
        self.assertFalse(R.c_did_get_hit(date(2000, 4, 30), p4))

        # Manny Ramirez tests (traded in 2008. This test checks to see
        #   if c_did_get_hit works for players in a year they are traded)
        self.assertTrue(R.c_did_get_hit(date(1994, 7, 26), p5))
        self.assertTrue(R.c_did_get_hit(date(2008, 5, 22), p5))
        self.assertTrue(R.c_did_get_hit(date(2008, 8, 1), p5))
        self.assertFalse(R.c_did_get_hit(date(1995, 6, 30), p5))
        self.assertFalse(R.c_did_get_hit(date(2008, 7, 29), p5))
        self.assertFalse(R.c_did_get_hit(date(2008, 8, 31), p5))

        ## Larry Jones, from Player, test. Tests to see if it works even if
        ## the player has a nickname (Goes by Chipper instead of Larry)
        pL = Player('jonesch06', 2003)
        self.assertTrue(R.c_did_get_hit(date(2003, 4, 19), pL))
        self.assertFalse(R.c_did_get_hit(date(2003, 8, 28), pL))

        # Test Miguel Cabrera, Asdrubal Cabrera, Delmon Young, Michael Young.
        # Checks for proper answer when the functional line of the boxscore
        # has two players with the same last name
        MC1 = Player("Miguel", "Cabrera", 2012)
        MC2 = Player("Asdrubal", "Cabrera", 2012)
        dateMC = date(2012, 9, 5)
        self.assertTrue(R.c_did_get_hit(dateMC, MC1))
        self.assertFalse(R.c_did_get_hit(dateMC, MC2))

        MY1 = Player("Michael", "Young", 2012)
        MY2 = Player("Delmon", "Young", 2012)
        dateMY = date(2012, 6, 26)
        self.assertTrue(R.c_did_get_hit(dateMY, MY1))
        self.assertFalse(R.c_did_get_hit(dateMY, MY2))

        ## Double Header tests (its a hit iff player got a hit in first game)
        self.assertFalse(R.c_did_get_hit(date(1996, 9, 25), p4)) # T1, H2
        self.assertFalse(R.c_did_get_hit(date(2008, 9, 7), p2)) # T1, T2
        self.assertTrue(R.c_did_get_hit(date(2007, 7, 28), p2)) # H1, T2
        self.assertTrue(R.c_did_get_hit(date(2006, 6, 3), p2)) # H1, H2

        # Lance Berkman tests
        Lance = Player("Lance", "Berkman", 2008)
        self.assertTrue(R.c_did_get_hit(date(2009, 7, 9), Lance))

        # To check that function safely exits on errors
        self.assertRaises(IOError, cfinish_did_get_hit, date=date(2012, 6, 5), 
            firstName='Faiyam', lastName='Rahman', boxscore='ooglyboogly.asdfx')
        self.assertRaises(EOFError, cfinish_did_get_hit, date=date(2012, 6, 5), 
            firstName='Faiyam', lastName='Rahman', 
            boxscore=Filepath.get_retrosheet_file(
                    folder='unzipped', fileF='boxscore', year=2012, 
                    team='NYN'))

        # Debugging an EOFError
        Eric = Player("Erick", "Aybar", 2010)
        Miguel = Player("Miguel", "Cabrera", 2010)
        self.assertFalse(R.c_did_get_hit(date(2010, 9, 4), Eric))
        self.assertTrue(R.c_did_get_hit(date(2010, 4, 23), Miguel))

    def test_cget_hit_info(self):

        ## Case 1 : (True, None); player got a hit on date d1
        d1 = date(2011, 9, 22)
        Jose = Player("Jose", "Altuve", 2011)
        R.create_player_hit_info_csv(Jose, 2011)
        self.assertEqual(cget_hit_info(date=d1, lahmanID=Jose.get_lahman_id()), 
                                       (True, None))

        ## Case 2: (False, None); player did not get a hit on date date
        d2 = date(2008, 9, 10)
        Will = Player("Will", "Venable", 2008)
        R.create_player_hit_info_csv(Will, 2008)
        self.assertEqual(cget_hit_info(date=d2, lahmanID=Will.get_lahman_id()), 
                                        (False, None))

        ## Case 3: ('pass', 'Suspended, Invalid'); player played in a suspended, invalid game
        d3 = date(2001, 7, 18)
        Mark = Player("Mark", "Grace", 2001)
        R.create_player_hit_info_csv(Mark, 2001)
        self.assertEqual(cget_hit_info(date=d3, lahmanID=Mark.get_lahman_id()), 
                                        ('pass', 'Suspended-Invalid.'))

        ## Case 4: (True, 'Suspended, Valid'); player got a hit in a suspended, valid game
        d4 = date(2010, 4, 16)
        Ben = Player("Ben", "Zobrist", 2010)
        R.create_player_hit_info_csv(Ben, 2010)
        self.assertEqual(cget_hit_info(date=d4, lahmanID=Ben.get_lahman_id()), 
                                        (True, 'Suspended-Valid.'))

        ## Case 5 : (False, 'Suspended, Valid'); player did not get a hit in a suspended, valid game
        Marco = Player("Marco", "Scutaro", 2010)
        R.create_player_hit_info_csv(Marco, 2010)
        self.assertEqual(cget_hit_info(date=d4, lahmanID=Marco.get_lahman_id()), 
          (False, 'Suspended-Valid.'))

    def test_cdid_start(self):
        Adrian = Player("Adrian", "Beltre", 2010)
        Craig = Player("Craig", "Biggio", 2004)
        for player, year in (
               (p1, 2011), (p2, 2011), (p1, 2004), (p2, 2006), (p1, 2009), 
               (Adrian, 2010), (Craig, 2004)):
            R.create_player_hit_info_csv(player, year)

        self.assertFalse(cdid_start(date=date(2011, 7, 2), lahmanID=p1.get_lahman_id()))
        self.assertTrue(cdid_start(date=date(2011, 9, 14), lahmanID=p2.get_lahman_id()))
        self.assertFalse(cdid_start(date=date(2004, 7, 4), lahmanID=p1.get_lahman_id()))
        self.assertTrue(cdid_start(date=date(2006, 4, 5), lahmanID=p2.get_lahman_id()))
        self.assertTrue(cdid_start(date=date(2009, 6, 17), lahmanID=p1.get_lahman_id()))
 
        # Adrian played in a game on 4/16 that was suspended and finished
        # on 4/17. He started on 4/16 and pinch ran on 4/17. Thus 
        # he should show up as NOT HAVING started on the 17th, and started on the 16th
        self.assertFalse(cdid_start(date=date(2010, 4, 17), lahmanID=Adrian.get_lahman_id()))
        self.assertTrue(cdid_start(date=date(2010, 4, 16), lahmanID=Adrian.get_lahman_id()))

        # Craig started on the 07/30 but only pinch hit on 7/31. Thus he should
        # show up as NOT having started on the 31st, and starting on the 30th
        self.assertFalse(cdid_start(date=date(2004, 7, 31), lahmanID=Craig.get_lahman_id()))
        self.assertTrue(cdid_start(date=date(2004, 7, 3), lahmanID=Craig.get_lahman_id()))

    def test_opposing_pitcher_era(self):
        JoseReyes = p2
        Pat = Player('Pat', 'Meares', 1997)
        Doug = Player('Doug', 'Mirabelli', 2000)
        Jacoby = Player('Jacoby', 'Ellsbury', 2012) 
        Ryan = Player('Ryan', 'Langerhans', 2011)
        David = Player("David", "Murphy", 2011)
        Jack = Player("Jack", "Wilson", 2005, debut='4/3/2001')
        Jeff = Player("Jeff", "Baker", 2011)
        for player, year in (
            (p2, 2009), (Pat, 1997), (Doug, 2000), (Jacoby, 2011), 
            (Ryan, 2011), (David, 2011), (Jack, 2005), (Jeff, 2011)):
            R.create_player_hit_info_csv(player, year)

        # Testing different points in the season
        self.assertEqual(copposing_pitcher_era(lahmanID=Ryan.get_lahman_id(), 
            date=date(2011,4,1)), float('inf')) # Opening Day
        self.assertEqual(float(copposing_pitcher_era(lahmanID=Pat.get_lahman_id(),
         date=date(1997,6,16))), 5.53) # Middle of the season
            # added bonus: pitcher has an asterisk next to his statline in the boxscore
        self.assertEqual(copposing_pitcher_era(lahmanID=Jacoby.get_lahman_id(),
         date=date(2011,9,28)), 4.85) # Closing Day

        # Testing home and away pitchers
        self.assertEqual(copposing_pitcher_era(lahmanID=JoseReyes.get_lahman_id(),
         date=date(2009,5,10)), 4.50) # visiting pitcher
        self.assertEqual(copposing_pitcher_era(lahmanID=Doug.get_lahman_id(),
         date=date(2000,9,27)), 1.69) # home pitcher

        # Testing multiple or single appeareacnes in the boxscore
            # Pitcher: CC Sabathia. ONLY PITCHED (All AL Games)
        self.assertEqual(copposing_pitcher_era(lahmanID=David.get_lahman_id(),
         date=date(2011, 4, 17)), 1.45)
            # Pitcher: Derek Lowe. PITCHED AND BATTED (NL Games)
        self.assertEqual(copposing_pitcher_era(lahmanID=Jack.get_lahman_id(),
         date=date(2005, 8, 5)), 3.99)
        
        # Pitcher with a multiword last name (motivated by a bug) -- Jorge De La Rosa
        # Double Whammy: He pitched in the SECOND game of a double header only, on 4/14
        self.assertEqual(copposing_pitcher_era(lahmanID=Jeff.get_lahman_id(),
         date=date(2011, 4, 26)), 3.00)

        # Another bug: 
        Endy = Player("Endy", "Chavez", 2001)
        R.create_player_hit_info_csv(Endy, 2001)
        self.assertEqual(copposing_pitcher_era(lahmanID=Endy.get_lahman_id(), 
            date=date(2001, 5, 29)), 6.72)
        self.assertEqual(copposing_pitcher_era(lahmanID=Endy.get_lahman_id(), 
            date=date(2001, 5, 29)), 6.72)
        self.assertEqual(copposing_pitcher_era(lahmanID=Endy.get_lahman_id(), 
            date=date(2001, 5, 29)), 6.72)