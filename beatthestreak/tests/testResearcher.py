import unittest

from datetime import date
from data import Data
from researcher import Researcher as R
from tests import setup, teardown, date, p1, p2, p3, p4, p5
from player import PlayerL, Player

participants_2012_3_28 = ["hallt901","nelsj901","hudsm901","belld901",
                          "wedge001","melvb001","wilht001","caria001",
                          "leagb001","ackld001","hernf002","mccab001",
                          "figgc001","ackld001","suzui001","smoaj001",
                          "montj003","carpm001","olivm001","saunm001",
                          "ryanb002","weekj001","pennc001","crisc001",
                          "smits002","suzuk001","reddj001","cespy001",
                          "alleb001","sogae001"]
# Below lists are massive
participants_2011_9_4 = ['randt901', 'porta901', 'vanol901', 'gormb901', 'mattd001', 'gonzf801', 'kimbc001', 'hawkb001', 'pradm001', 'kersc001', 'delgr001', 'gordd002', 'lonej001', 'kempm001', 'rivej001', 'ethia001', 'milea001', 'barar001', 'sellj002', 'kersc001', 'bourm001', 'pradm001', 'diazm003', 'uggld001', 'rossd001', 'gonza002', 'wilsj002', 'consj001', 'delgr001', 'blasc901', 'wolfj901', 'reybd901', 'kulpr901', 'hurdc001', 'quadm801', 'wellr001', 'mortc002', 'marss002', 'casts001', 'mortc002', 'wellr001', 'presa001', 'harrj002', 'mccua001', 'walkn001', 'joneg002', 'ceder002', 'mckem001', 'mortc002', 'casts001', 'campt001', 'ramia001', 'penac001', 'lahab001', 'byrdm001', 'barnd001', 'hillk002', 'wellr001', 'fairc901', 'westj901', 'holbs901', 'schrp901', 'manuc101', 'mckej801', 'hensc002', 'hernd003', 'camem001', 'hallr001', 'sanca004', 'victs001', 'martm003', 'utlec001', 'howar001', 'pench001', 'ibanr001', 'ruizc001', 'valdw001', 'hallr001', 'bonie001', 'infao001', 'dobbg001', 'sancg001', 'morrl001', 'camem001', 'peteb001', 'buckj001', 'sanca004', 'nauep901', 'eddid901', 'demud901', 'danlk901', 'roenr001', 'millb101', 'marcs001', 'rodrw002', 'braur002', 'marcs001', 'rodrw002', 'hartc001', 'hairj002', 'braur002', 'fielp001', 'mcgec001', 'betay001', 'lucrj001', 'gomec002', 'marcs001', 'schaj002', 'parej002', 'martj006', 'bogub001', 'downm001', 'wallb001', 'barmc001', 'corpc001', 'rodrw002', 'hirsj901', 'bellw901', 'carav901', 'diazl901', 'tracj101', 'blacb001', 'latom001', 'cooka002', 'hermj001', 'cooka002', 'latom001', 'fowld001', 'ellim001', 'gonzc001', 'tulot001', 'giamj001', 'smits002', 'kouzk001', 'alfoe002', 'cooka002', 'venaw001', 'bartj001', 'hudso001', 'guzmj005', 'hermj001', 'rizza001', 'parra001', 'martl002', 'latom001', 'knigb901', 'laynj901', 'davib902', 'wendh902', 'gibsk001', 'bochb002', 'hudsd001', 'voger001', 'putzj001', 'bloow001', 'hudsd001', 'voger001', 'bloow001', 'hilla001', 'uptoj001', 'montm001', 'goldp001', 'younc004', 'rober002', 'parrg001', 'hudsd001', 'rossc001', 'keppj001', 'beltc001', 'sandp001', 'huffa001', 'beltb001', 'cabro001', 'white004', 'voger001', 'buckc901', 'iassd901', 'mealj901', 'campa902', 'baked002', 'larut101', 'brayb001', 'salaf001', 'cordf002', 'franj005', 'arrob001', 'jacke001', 'philb001', 'rente001', 'vottj001', 'brucj001', 'alony001', 'stubd001', 'franj005', 'hanir001', 'arrob001', 'furcr001', 'pujoa001', 'hollm001', 'berkl001', 'schus001', 'lairg001', 'descd001', 'jacke001', 'onorb901', 'marqa901', 'wegnm901', 'rapue901', 'collt801', 'johnd105', 'igarr001', 'hernl003', 'parnb001', 'harrw001', 'pelfm001', 'hernl003', 'tejar001', 'turnj001', 'dudal001', 'wrigd002', 'pagaa001', 'satij001', 'nickm001', 'pelfm001', 'desmi001', 'bernr001', 'zimmr001', 'wertj001', 'ankir001', 'espid001', 'marrc001', 'ramow001', 'hernl003', 'wintm901', 'everm901', 'guccc901', 'muchm901', 'gardr001', 'sciom001', 'pinej001', 'slowk001', 'waldj001', 'abreb001', 'slowk001', 'pinej001', 'reveb001', 'plout001', 'mauej001', 'cuddm001', 'kubej002', 'valed001', 'hughl001', 'nisht001', 'buted001', 'aybae001', 'kendh001', 'abreb001', 'huntt001', 'trumm001', 'wellv001', 'calla001', 'troum001', 'congh001', 'drecb901', 'emmep901', 'drakr901', 'darlg901', 'washr001', 'frant001', 'harrm001', 'lackj001', 'napom001', 'harrm001', 'lackj001', 'kinsi001', 'andre001', 'hamij003', 'younm003', 'belta001', 'murpd005', 'napom001', 'morem001', 'chave002', 'ellsj001', 'pedrd001', 'gonza003', 'youkk001', 'ortid001', 'jackc002', 'crawc002', 'saltj001', 'scutm001', 'coope901', 'estam901', 'timmt901', 'kellj901', 'guilo001', 'leylj801', 'schem001', 'buehm001', 'martv001', 'buehm001', 'schem001', 'pierj002', 'ramia003', 'konep001', 'piera001', 'vicid001', 'riosa002', 'deaza001', 'moreb001', 'beckg001', 'jacka001', 'ordom001', 'yound003', 'cabrm001', 'martv001', 'avila001', 'peraj001', 'rabur001', 'ingeb001', 'welkt901', 'fleta901', 'reynj901', 'dimum901', 'actam801', 'yoste001', 'gomej002', 'franj003', 'perec002', 'donaj002', 'gomej002', 'franj003', 'carre001', 'fukuk001', 'cabra002', 'santc002', 'duncs001', 'donaj002', 'hannj001', 'marsl001', 'headj001', 'gorda001', 'cabrm002', 'butlb003', 'hosme001', 'giavj001', 'mousm001', 'penab002', 'maiem001', 'getzc001', 'hallt901', 'millb901', 'hoyej901', 'cuzzp901', 'wakad001', 'giraj001', 'sabac001', 'cecib001', 'cecib001', 'sabac001', 'mccom001', 'johnk003', 'bautj002', 'encae001', 'lawrb002', 'teahm001', 'molij001', 'arenj001', 'wised001', 'gardb001', 'jeted001', 'teixm001', 'rodra001', 'canor001', 'swisn001', 'jonea002', 'martr004', 'montj003', 'tscht901', 'nelsj901', 'fostm901', 'welkb901', 'wedge001', 'melvb001', 'cahit001', 'beavb001', 'baila001', 'suzuk001', 'beavb001', 'cahit001', 'suzui001', 'gutif001', 'ackld001', 'carpm001', 'smoaj001', 'olivm001', 'seagk001', 'wellc001', 'rodrl002', 'weekj001', 'pennc001', 'matsh001', 'willj004', 'dejed001', 'alleb001', 'sweer001', 'suzuk001', 'sizes001', 'johna901', 'culbf901', 'cedeg901', 'barkl901', 'showb801', 'maddj801', 'hellj001', 'guthj001', 'rodrs002', 'guthj001', 'hellj001', 'anglm001', 'hardj003', 'markn001', 'jonea003', 'guerv001', 'reynm001', 'andir001', 'hudsk001', 'tatuc001', 'jennd002', 'damoj001', 'longe001', 'joycm001', 'lobaj001', 'kotcc001', 'guyeb001', 'brigr001', 'rodrs002']
participants_2013_6_7 = ['reynj901', 'hoyej901', 'hirsj901', 'davib902', 'melvb001', 'coopd001', 'parkj001', 'salec001', 'balfg001', 'donaj001', 'parkj001', 'salec001', 'crisc001', 'lowrj001', 'cespy001', 'donaj001', 'frein001', 'younc004', 'reddj001', 'norrd001', 'rosaa001', 'deaza001', 'ramia003', 'riosa002', 'dunna001', 'vicid001', 'gillc001', 'beckg001', 'dankj002', 'flowt001', 'holbs901', 'fleta901', 'drakr901', 'westj901', 'frant001', 'leylj801', 'verlj001', 'jimeu001', 'martv001', 'jimeu001', 'verlj001', 'bourm001', 'kipnj001', 'swisn001', 'branm003', 'santc002', 'reynm001', 'giamj001', 'avilm001', 'stubd001', 'dirka001', 'huntt001', 'cabrm001', 'fielp001', 'martv001', 'peraj001', 'penab002', 'santr002', 'garca003', 'gormb901', 'gonzm901', 'randt901', 'vanol901', 'portb001', 'yoste001', 'herrk001', 'wrigw001', 'hollg001', 'butlb003', 'lylej001', 'shiej002', 'barnb002', 'crowt001', 'castj006', 'martj006', 'penac001', 'cartc002', 'ceder002', 'domim001', 'gonzm002', 'gorda001', 'hosme001', 'peres002', 'butlb003', 'cainl001', 'lougd001', 'tejam001', 'getzc001', 'escoa003', 'wegnm901', 'diazl901', 'muchm901', 'wintm901', 'giraj001', 'wedge001', 'bondj001', 'kuroh001', 'wilht001', 'ryanb002', 'kuroh001', 'bondj001', 'gardb001', 'canor001', 'teixm001', 'hafnt001', 'youkk001', 'wellv001', 'suzui001', 'brigr001', 'stewc001', 'chave002', 'seagk001', 'morak001', 'ibanr001', 'morsm001', 'frann001', 'shopk001', 'ryanb002', 'barrl901', 'barkl901', 'cedeg901', 'carav901', 'showb801', 'maddj801', 'archc001', 'hammj002', 'rodnf001', 'jennd002', 'hammj002', 'archc001', 'mclon001', 'machm001', 'markn001', 'jonea003', 'davic003', 'wietm001', 'hardj003', 'dickc001', 'flahr001', 'joycm001', 'zobrb001', 'johnk003', 'longe001', 'lonej001', 'jennd002', 'scotl001', 'molij001', 'escoy001', 'mealj901', 'drecb901', 'darlg901', 'emmep901', 'washr001', 'gibbj001', 'wagnn001', 'tepen001', 'encae001', 'tepen001', 'rogee002', 'andre001', 'profj001', 'piera001', 'belta001', 'bakej001', 'murpd005', 'gentc001', 'mcguc001', 'martl004', 'cabrm002', 'bautj002', 'encae001', 'linda001', 'arenj001', 'rasmc001', 'iztum001', 'bonie001', 'kawam001', 'porta901', 'laynj901', 'gibsg901', 'wendh902', 'bochb002', 'gibsk001', 'ziegb001', 'affej001', 'bellh001', 'goldp001', 'cainm001', 'corbp001', 'torra001', 'scutm001', 'poseb001', 'pench001', 'sandp001', 'beltb001', 'crawb001', 'blang001', 'cainm001', 'parrg001', 'bloow001', 'goldp001', 'montm001', 'rossc001', 'pradm001', 'gregd001', 'polla001', 'corbp001', 'gibsg901', 'bakej902', 'demud901', 'nauep901', 'herna901', 'hurdc001', 'sveud001', 'lirif001', 'woodt004', 'grilj001', 'martr004', 'lirif001', 'woodt004', 'marts002', 'mercj002', 'mccua001', 'sancg001', 'martr004', 'alvap001', 'walkn001', 'snidt001', 'lirif001', 'barnd001', 'ransc001', 'rizza001', 'soria001', 'hairs001', 'castw002', 'casts001', 'sweer001', 'woodt004', 'guccc901', 'estam901', 'cuzzp901', 'hallt901', 'mathm001', 'baked002', 'waina001', 'leakm001', 'freed001', 'waina001', 'leakm001', 'carpm002', 'beltc001', 'hollm001', 'craia001', 'moliy001', 'freed001', 'kozmp001', 'waina001', 'choos001', 'cozaz001', 'vottj001', 'philb001', 'brucj001', 'frazt001', 'paulx001', 'mesod001', 'leakm001', 'hicke901', 'joycj901', 'blasc901', 'nelsj901', 'blacb001', 'weisw001', 'belim001', 'thatj001', 'arenn001', 'volqe001', 'delaj001', 'denoc001', 'cabre001', 'headc001', 'quenc001', 'gyorj001', 'blank002', 'maybc001', 'grany001', 'volqe001', 'fowld001', 'youne003', 'gonzc001', 'tulot001', 'heltt001', 'arenn001', 'lemad001', 'torry001', 'delaj001', 'scotd901', 'buckc901', 'reybd901', 'ticht901', 'gonzf801', 'mattd001', 'leagb001', 'varva001', 'mahop002', 'simma001', 'heywj001', 'uptoj001', 'freef001', 'gatte001', 'johnc003', 'uggld001', 'uptob001', 'mahop002', 'puigy001', 'ellim001', 'gonza003', 'vanss001', 'hairj002', 'ethia001', 'hernr002', 'cruzl001', 'tumpj901', 'carlm901', 'knigb901', 'iassd901', 'manuc101', 'roenr001', 'rodrf003', 'horsj001', 'ramia001', 'figaa001', 'younm003', 'maybj001', 'rollj001', 'howar001', 'browd004', 'yound003', 'krate001', 'galvf001', 'aokin001', 'seguj002', 'braur002', 'ramia001', 'lucrj001', 'gomec002', 'weekr001', 'betay001', 'figaa001']

class TestResearcher(unittest.TestCase):
    
    def setUp(self):
        setup()
        
    def tearDown(self):
        teardown()
    
    # def test_get_participants(self):
    # 	self.assertEqual(R.get_participants(date(2011,9,4)), 
    #     	             participants_2011_9_4)
    #     self.assertEqual(R.get_participants(date(2012,3,28)), 
    #     	             participants_2012_3_28)
    #     self.assertEqual(R.get_participants(date(2013,6,7)), 
    #     	             participants_2013_6_7)

    def test_find_home_team(self):
    	self.assertEqual(R.find_home_team(date(2011, 8, 3), p1), "MIL")
        self.assertEqual(R.find_home_team(date(2012, 5, 2), p1), "WAS")
        self.assertEqual(R.find_home_team(date(2012, 6, 15), p2), "TBA")
        self.assertEqual(R.find_home_team(date(2013, 9, 20), p2), "BOS")

    # def test_did_start(self):
    #     self.assertFalse(R.did_start(date(2011, 7, 2), p1))
    #     self.assertTrue(R.did_start(date(2011, 9, 14), p2))
    #     self.assertFalse(R.did_start(date(2012, 4, 15), p1))
    #     self.assertTrue(R.did_start(date(2012, 4, 15), p2))
    #     self.assertTrue(R.did_start(date(2013, 5, 17), p1))
    #     self.assertTrue(R.did_start(date(2013, 8, 11), p2))
    
    # # @skip("time consuming")
    # def test_did_get_hit(self):
    # 	# Edwin Jackon test
    #     self.assertFalse(R.did_get_hit(date(2012, 5, 2), p1))

    #     # Jose Reyes Tests
    #     self.assertTrue(R.did_get_hit(date(2012, 6, 16), p2))
    #     self.assertTrue(R.did_get_hit(date(2005, 4, 4), p2))
    #     self.assertTrue(R.did_get_hit(date(2003, 7, 12), p2))
    #     self.assertFalse(R.did_get_hit(date(2012, 6, 15), p2))
    #     self.assertFalse(R.did_get_hit(date(2008, 9, 21), p2))

    #     # Alfonso Soriano Tests
    #     self.assertTrue(R.did_get_hit(date(2003, 3, 31), p3))
    #     self.assertTrue(R.did_get_hit(date(2009, 5, 12), p3))
    #     self.assertFalse(R.did_get_hit(date(2001, 9, 4), p3))
    #     self.assertFalse(R.did_get_hit(date(2007, 7, 20), p3))
    #     self.assertFalse(R.did_get_hit(date(2004, 9, 16), p3))

    #     # Jorge Posada tests
    #     self.assertTrue(R.did_get_hit(date(2004, 8, 17), p4))
    #     self.assertTrue(R.did_get_hit(date(2010, 7, 11), p4))
    #     self.assertFalse(R.did_get_hit(date(1997, 5, 23), p4))
    #     self.assertFalse(R.did_get_hit(date(2000, 4, 30), p4))

    #     # Manny Ramirez tests (traded in 2008. This test checks to see
    #     # 	if did_get_hit works for players in a year they are traded)
    #     self.assertTrue(R.did_get_hit(date(1994, 7, 26), p5))
    #     self.assertTrue(R.did_get_hit(date(2008, 5, 22), p5))
    #     self.assertTrue(R.did_get_hit(date(2008, 8, 1), p5))
    #     self.assertFalse(R.did_get_hit(date(1995, 6, 30), p5))
    #     self.assertFalse(R.did_get_hit(date(2008, 7, 29), p5))
    #     self.assertFalse(R.did_get_hit(date(2008, 8, 31), p5))

    #     ## Larry Jones, from PlayerL, test. Tests to see if it works even if
    #     ## the player has a nickname (Goes by Chipper instead of Larry)
    #     pL = PlayerL('jonesch06', 2003)
    #     pL = Player(0, playerL=pL)
    #     self.assertTrue(R.did_get_hit(date(2003, 4, 19), pL))
    #     self.assertFalse(R.did_get_hit(date(2003, 8, 28), pL))

    #     # Double Header tests (its a hit iff player got a hit in first game)
    #     self.assertFalse(R.did_get_hit(date(1996, 9, 25), p4)) # T1, H2
    #     self.assertFalse(R.did_get_hit(date(2008, 9, 7), p2)) # T1, T2
    #     self.assertTrue(R.did_get_hit(date(2007, 7, 28), p2)) # H1, T2
    #     self.assertTrue(R.did_get_hit(date(2006, 6, 3), p2)) # H1, H2

    # def test_num_at_bats(self):
    #     self.assertEqual(R.num_at_bats(2010, p1), 38) # traded from NL to AL
    #     self.assertEqual(R.num_at_bats(2006, p2), 647)
    #     self.assertEqual(R.num_at_bats(2005, p3), 637)
    #     self.assertEqual(R.num_at_bats(2001, p4), 484)
    #     self.assertEqual(R.num_at_bats(2008, p5), 552) # traded from BOS to LAD

    # def test_num_plate_appearances(self):
    #     self.assertEqual(R.num_plate_appearances(2010, p1), 43) # traded from NL to AL
    #     self.assertEqual(R.num_plate_appearances(2006, p2), 703)
    #     self.assertEqual(R.num_plate_appearances(2005, p3), 682)
    #     self.assertEqual(R.num_plate_appearances(2001, p4), 557)
    #     self.assertEqual(R.num_plate_appearances(2008, p5), 654) # traded from BOS to LAD

    # def test_name_from_lahman_id(self):
    #     self.assertEqual(R.name_from_lahman_id("jacksed01"), ("Edwin", "Jackson"))
    #     self.assertEqual(R.name_from_lahman_id("reyesjo01"), ("Jose",  "Reyes"))
    #     self.assertEqual(R.name_from_lahman_id("soriaal01"), ("Alfonso", "Soriano"))
    #     self.assertEqual(R.name_from_lahman_id("posadjo01"), ("Jorge", "Posada"))
    #     self.assertEqual(R.name_from_lahman_id("ramirma02"), ("Manny", "Ramirez"))
    #     self.assertEqual(R.name_from_lahman_id("loducpa01"), ("Paul", "Lo Duca"))

    def test_get_opening_day(self):
        self.assertEqual(R.get_opening_day(2010), date(2010,4,4))
        self.assertEqual(R.get_opening_day(1992), date(1992, 4,6))

    def test_get_closing_day(self):
        self.assertEqual(R.get_closing_day(2010), date(2010,10,3))
        self.assertEqual(R.get_closing_day(1992), date(1992, 10,4))