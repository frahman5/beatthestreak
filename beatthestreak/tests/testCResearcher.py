import unittest
from datetime import date
from beatthestreak.tests import p1, p2, p3, p4, p5

from beatthestreak.researcher import Researcher as R
from beatthestreak.player import Player
from beatthestreak.filepath import Filepath
from cresearcher import cfinish_did_get_hit, cget_hit_info

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

    def test_c_boxscore_buffer(self):
        d1 = date(2012, 6, 17)
        d2 = date(2012, 6, 15)
        d3 = date(2012, 8, 9)
        Albert = Player("Albert", "Pujols", 2012)
        Jose = p2
        Colby = Player("Colby", "Rasmus", 2012)
        
        ## CHECK 1: If a team's info is not on the buffer, then startSeekPos
        ## is 0 and boxscore buffer is updated
            ## Check 1.1: If it's a new year, startSeekPos = 0 and boxscore 
            ## buffer is set to [year, {'team': lastByteChecked}]
        R.boxscoreBuffer = [2010, {}] # 2010 on buffer
        R.did_get_hit(d1, Albert)
        self.assertEqual(R.boxscoreBuffer, [2012, {'ANA': (d1, 53499)}])
        self.assertEqual(R.type1SeekPosUsed, 0)
            ## Check 1.2: If its the same year but the team's boxscore has not
            ## yet been opened, startSeekPos = 0 and team is added to 
            ## boxscoreBuffer[1].keys
        self.assertEqual(R.boxscoreBuffer, [2012, {'ANA': (d1, 53499)}])
        R.did_get_hit(d2, Jose)
        self.assertEqual(R.boxscoreBuffer, 
            [2012, {'ANA': (d1, 53499), 'TBA': (d2, 57767)}])
        self.assertEqual(R.type1SeekPosUsed, 0)

        ## CHECK 2: if a team's boxscore info is on the buffer, then their
        ## info is examined on the buffer
            ## Check 2.1: If date is GREATER than date on buffer, startSeekPos 
            ## = boxscoreBuffer[1][team][1] and buffer's last byte checked 
            ## is updated
        self.assertEqual(R.boxscoreBuffer, 
            [2012, {'ANA': (d1, 53499), 'TBA': (d2, 57767)}])
        R.did_get_hit(d3, Colby)
        self.assertEqual(R.boxscoreBuffer, 
            [2012, {'ANA': (d1, 53499), 'TBA': (d3, 101880)}])
        self.assertEqual(R.type1SeekPosUsed, 57767)

            ## CHECK 2.2: if date is less than date on buffer, startSeekPos = 0
            ## and last byte checked is updated
        self.assertEqual(R.boxscoreBuffer, 
            [2012, {'ANA': (d1, 53499), 'TBA': (d3, 101880)}])
        R.did_get_hit(d2, Jose)
        self.assertEqual(R.boxscoreBuffer, 
            [2012, {'ANA': (d1, 53499), 'TBA': (d2, 57767)}])
        self.assertEqual(R.type1SeekPosUsed, 0) 


            ## Check 2.3: If date is EQUAL to date on buffer, startSeekPos = 0
            ## and last byte checked is the SAME
        self.assertEqual(R.boxscoreBuffer, 
            [2012, {'ANA': (d1, 53499), 'TBA': (d2, 57767)}])
        R.did_get_hit(d2, Jose)
        self.assertEqual(R.boxscoreBuffer, 
            [2012, {'ANA': (d1, 53499), 'TBA': (d2, 57767)}])
        self.assertEqual(R.type1SeekPosUsed, 0)  

    def test_c_cget_hit_info(self):
        d1 = date(2012, 4, 15)
        d2 = date(2001, 7, 18)
        d3 = date(2010, 4, 16)
        d4 = date(2012, 7, 3)

        ## Case 1 : (True, None); player got a hit on date d1
        Jose = Player("Jose", "Altuve", 2012)
        R.create_player_hit_info_csv(Jose, 2012)
        self.assertEqual(cget_hit_info(date=d1, lahmanID=Jose.get_lahman_id()), 
                                       (True, None))

        ## Case 2: (False, None); player did not get a hit on date date
        Will = Player("Will", "Venable", 2012)
        R.create_player_hit_info_csv(Will, 2012)
        self.assertEqual(cget_hit_info(date=d4, lahmanID=Will.get_lahman_id()), 
                                        (False, None))

        ## Case 3: ('pass', 'Suspended, Invalid'); player played in a suspended, invalid game
        Mark = Player("Mark", "Grace", 2001)
        R.create_player_hit_info_csv(Mark, 2001)
        self.assertEqual(cget_hit_info(date=d2, lahmanID=Mark.get_lahman_id()), 
                                        ('pass', 'Suspended-Invalid.'))

        ## Case 4: (True, 'Suspended, Valid'); player got a hit in a suspended, valid game
        Ben = Player("Ben", "Zobrist", 2010)
        R.create_player_hit_info_csv(Ben, 2010)
        self.assertEqual(cget_hit_info(date=d3, lahmanID=Ben.get_lahman_id()), 
                                        (True, 'Suspended-Valid.'))

        ## Case 5 : (False, 'Suspended, Valid'); player did not get a hit in a suspended, valid game
        Marco = Player("Marco", "Scutaro", 2010)
        R.create_player_hit_info_csv(Marco, 2010)
        self.assertEqual(cget_hit_info(date=d3, lahmanID=Marco.get_lahman_id()), 
                                        (False, 'Suspended-Valid.'))