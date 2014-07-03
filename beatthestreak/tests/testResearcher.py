import unittest
import os
import datetime

from datetime import date
from pandas import DataFrame, to_datetime

from beatthestreak.filepath import Filepath
from beatthestreak.researcher import Researcher as R
from beatthestreak.tests import setup, teardown, p1, p2, p3, p4, p5
from beatthestreak.player import Player
from beatthestreak.exception import FileContentException, BadDateException, \
    NotSuspendedGameException, SusGameDoesntFitCategoryException

participants_2012_3_28 = ["hallt901","nelsj901","hudsm901","belld901",
                          "wedge001","melvb001","wilht001","caria001",
                          "leagb001","ackld001","hernf002","mccab001",
                          "figgc001","ackld001","suzui001","smoaj001",
                          "montj003","carpm001","olivm001","saunm001",
                          "ryanb002","weekj001","pennc001","crisc001",
                          "smits002","suzuk001","reddj001","cespy001",
                          "alleb001","sogae001"]
# Below lists are massive
participants_2011_9_4 = ['randt901', 'porta901', 'vanol901', 'gormb901', 'mattd001', 'gonzf801', 'kimbc001', 'hawkb001', 'pradm001', 'kersc001', 'delgr001', 'gordd002', 'lonej001', 'kempm001', 'rivej001', 'ethia001', 'milea001', 'barar001', 'sellj002', 'kersc001', 'bourm001', 'pradm001', 'diazm003', 'uggld001', 'rossd001', 'gonza002', 'wilsj002', 'consj001', 'delgr001', 'blasc901', 'wolfj901', 'reybd901', 'kulpr901', 'hurdc001', 'quadm801', 'wellr001', 'mortc002', 'marss002', 'casts001', 'mortc002', 'wellr001', 'presa001', 'harrj002', 'mccua001', 'lee-d002', 'walkn001', 'joneg002', 'ceder002', 'mckem001', 'mortc002', 'casts001', 'campt001', 'ramia001', 'penac001', 'lahab001', 'byrdm001', 'barnd001', 'hillk002', 'wellr001', 'fairc901', 'westj901', 'holbs901', 'schrp901', 'manuc101', 'mckej801', 'hensc002', 'hernd003', 'camem001', 'hallr001', 'sanca004', 'victs001', 'martm003', 'utlec001', 'howar001', 'pench001', 'ibanr001', 'ruizc001', 'valdw001', 'hallr001', 'bonie001', 'infao001', 'dobbg001', 'sancg001', 'morrl001', 'camem001', 'peteb001', 'buckj001', 'sanca004', 'nauep901', 'eddid901', 'demud901', 'danlk901', 'roenr001', 'millb101', 'marcs001', 'rodrw002', 'braur002', 'marcs001', 'rodrw002', 'hartc001', 'hairj002', 'braur002', 'fielp001', 'mcgec001', 'betay001', 'lucrj001', 'gomec002', 'marcs001', 'schaj002', 'parej002', 'martj006', 'bogub001', 'downm001', 'wallb001', 'barmc001', 'corpc001', 'rodrw002', 'hirsj901', 'bellw901', 'carav901', 'diazl901', 'tracj101', 'blacb001', 'latom001', 'cooka002', 'hermj001', 'cooka002', 'latom001', 'fowld001', 'ellim001', 'gonzc001', 'tulot001', 'giamj001', 'smits002', 'kouzk001', 'alfoe002', 'cooka002', 'venaw001', 'bartj001', 'hudso001', 'guzmj005', 'hermj001', 'rizza001', 'parra001', 'martl002', 'latom001', 'knigb901', 'laynj901', 'davib902', 'wendh902', 'gibsk001', 'bochb002', 'hudsd001', 'voger001', 'putzj001', 'bloow001', 'hudsd001', 'voger001', 'bloow001', 'hilla001', 'uptoj001', 'montm001', 'goldp001', 'younc004', 'rober002', 'parrg001', 'hudsd001', 'rossc001', 'keppj001', 'beltc001', 'sandp001', 'huffa001', 'beltb001', 'cabro001', 'white004', 'voger001', 'buckc901', 'iassd901', 'mealj901', 'campa902', 'baked002', 'larut101', 'brayb001', 'salaf001', 'cordf002', 'franj005', 'arrob001', 'jacke001', 'philb001', 'rente001', 'vottj001', 'brucj001', 'alony001', 'stubd001', 'franj005', 'hanir001', 'arrob001', 'furcr001', 'jay-j001', 'pujoa001', 'hollm001', 'berkl001', 'schus001', 'lairg001', 'descd001', 'jacke001', 'onorb901', 'marqa901', 'wegnm901', 'rapue901', 'collt801', 'johnd105', 'igarr001', 'hernl003', 'parnb001', 'harrw001', 'pelfm001', 'hernl003', 'tejar001', 'turnj001', 'dudal001', 'wrigd002', 'pagaa001', 'bay-j001','satij001', 'nickm001', 'pelfm001', 'desmi001', 'bernr001', 'zimmr001', 'wertj001', 'ankir001', 'espid001', 'marrc001', 'ramow001', 'hernl003', 'wintm901', 'everm901', 'guccc901', 'muchm901', 'gardr001', 'sciom001', 'pinej001', 'slowk001', 'waldj001', 'abreb001', 'slowk001', 'pinej001', 'reveb001', 'plout001', 'mauej001', 'cuddm001', 'kubej002', 'valed001', 'hughl001', 'nisht001', 'buted001', 'aybae001', 'kendh001', 'abreb001', 'huntt001', 'trumm001', 'wellv001', 'calla001', 'troum001', 'congh001', 'drecb901', 'emmep901', 'drakr901', 'darlg901', 'washr001', 'frant001', 'harrm001', 'lackj001', 'napom001', 'harrm001', 'lackj001', 'kinsi001', 'andre001', 'hamij003', 'younm003', 'belta001', 'murpd005', 'napom001', 'morem001', 'chave002', 'ellsj001', 'pedrd001', 'gonza003', 'youkk001', 'ortid001', 'jackc002', 'crawc002', 'saltj001', 'scutm001', 'coope901', 'estam901', 'timmt901', 'kellj901', 'guilo001', 'leylj801', 'schem001', 'buehm001', 'martv001', 'buehm001', 'schem001', 'pierj002', 'ramia003', 'konep001', 'piera001', 'vicid001', 'riosa002', 'deaza001', 'moreb001', 'beckg001', 'jacka001', 'ordom001', 'yound003', 'cabrm001', 'martv001', 'avila001', 'peraj001', 'rabur001', 'ingeb001', 'welkt901', 'fleta901', 'reynj901', 'dimum901', 'actam801', 'yoste001', 'gomej002', 'franj003', 'perec002', 'donaj002', 'gomej002', 'franj003', 'carre001', 'fukuk001', 'cabra002', 'santc002', 'duncs001', 'donaj002', 'hannj001', 'marsl001', 'headj001', 'gorda001', 'cabrm002', 'butlb003', 'hosme001', 'giavj001', 'mousm001', 'penab002', 'maiem001', 'getzc001', 'hallt901', 'millb901', 'hoyej901', 'cuzzp901', 'wakad001', 'giraj001', 'sabac001', 'cecib001', 'cecib001', 'sabac001', 'mccom001', 'johnk003', 'bautj002', 'encae001', 'lawrb002', 'teahm001', 'molij001', 'arenj001', 'wised001', 'gardb001', 'jeted001', 'teixm001', 'rodra001', 'canor001', 'swisn001', 'jonea002', 'martr004', 'montj003', 'tscht901', 'nelsj901', 'fostm901', 'welkb901', 'wedge001', 'melvb001', 'cahit001', 'beavb001', 'baila001', 'suzuk001', 'beavb001', 'cahit001', 'suzui001', 'gutif001', 'ackld001', 'carpm001', 'smoaj001', 'olivm001', 'seagk001', 'wellc001', 'rodrl002', 'weekj001', 'pennc001', 'matsh001', 'willj004', 'dejed001', 'alleb001', 'sweer001', 'suzuk001', 'sizes001', 'johna901', 'culbf901', 'cedeg901', 'barkl901', 'showb801', 'maddj801', 'hellj001', 'guthj001', 'rodrs002', 'guthj001', 'hellj001', 'anglm001', 'hardj003', 'markn001', 'jonea003', 'guerv001', 'reynm001', 'andir001', 'hudsk001', 'tatuc001', 'jennd002', 'damoj001', 'longe001', 'joycm001', 'lobaj001', 'kotcc001', 'guyeb001', 'brigr001', 'rodrs002']
participants_2009_7_9 = ['meric901', 'diazl901', 'coope901', 'reilm901', 'gonzf801', 'hinca001', 'calek001', 'schos001', 'carrb001', 'milla002', 'petiy001', 'coghc001', 'bonie001', 'uggld001', 'cantj001', 'rossc001', 'hermj001', 'bakej002', 'helmw001', 'milla002', 'lopef001', 'ojeda001', 'uptoj001', 'reynm001', 'parrg001', 'younc004', 'clart002', 'carll001', 'petiy001', 'drakr901', 'schrp901', 'nauep901', 'westj901', 'cox-b103', 'tracj101', 'rincj001', 'gonzm001', 'streh001', 'atkig001', 'hanst001', 'cooka002', 'mclon001', 'pradm001', 'andeg001', 'mccab002', 'escoy001', 'kotcc001', 'franj004', 'conrb001', 'hanst001', 'fowld001', 'barmc001', 'heltt001', 'hawpb001', 'tulot001', 'stewi001', 'iannc001', 'gonzc001', 'cooka002', 'wolfj901', 'onorb901', 'culbf901', 'johna901', 'actam801', 'coopc001', 'ariaa002', 'lannj001', 'bourm001', 'lannj001', 'ortir001', 'morgn001', 'johnn001', 'zimmr001', 'dunna001', 'willj004', 'guzmc001', 'bardj001', 'herna003', 'lannj001', 'bourm001', 'tejam001', 'berkl001', 'lee-c001', 'pench001', 'rodri001', 'blumg001', 'keppj001', 'ortir001', 'emmep901', 'darlg901', 'hohnb901', 'drecb901', 'larut101', 'machk101', 'pinej001', 'villc001', 'pujoa001', 'pinej001', 'parrm001', 'ryanb002', 'rasmc001', 'pujoa001', 'ludwr001', 'stavn001', 'moliy001', 'hoffj002', 'pinej001', 'bardb001', 'counc001', 'hardj003', 'braur002', 'fielp001', 'mcgec001', 'camem001', 'cataf001', 'rivem003', 'parrm001', 'fostm901', 'fairc901', 'hirsj901', 'bellw901', 'torrj101', 'manuj101', 'wolfr001', 'hernl003', 'ramim002', 'wolfr001', 'hernl003', 'furcr001', 'ethia001', 'ramim002', 'blakc001', 'lonej001', 'martr004', 'hudso001', 'kempm001', 'wolfr001', 'castl001', 'evann001', 'wrigd002', 'shefg001', 'tatif001', 'churr001', 'santo001', 'coraa001', 'hernl003', 'scotd901', 'mealj901', 'dimum901', 'kulpr901', 'baked002', 'manuc101', 'moyej001', 'owinm001', 'lidgb001', 'rollj001', 'owinm001', 'moyej001', 'tavew001', 'dickc001', 'vottj001', 'philb001', 'hernr002', 'gomej001', 'encae001', 'janip001', 'owinm001', 'rollj001', 'victs001', 'utlec001', 'howar001', 'wertj001', 'dobbg001', 'felip001', 'ruizc001', 'moyej001', 'cuzzp901', 'rungb901', 'hallt901', 'campa902', 'blacb001', 'bochb002', 'linct001', 'geerj001', 'molib001', 'geerj001', 'linct001', 'cabre001', 'gwynt002', 'gonza003', 'kouzk001', 'headc001', 'venaw001', 'alfoe002', 'rodrl002', 'geerj001', 'winnr001', 'schin001', 'sandp001', 'molib001', 'bowkj001', 'rente001', 'ishit001', 'uribj002', 'linct001', 'millb901', 'cousd901', 'ticht901', 'joycj901', 'hillt801', 'frant001', 'hochl001', 'mastj001', 'sorij001', 'dejed001', 'hochl001', 'pennb002', 'dejed001', 'bloow001', 'butlb003', 'guilj001', 'teahm001', 'jacom001', 'olivm001', 'calla001', 'freer001', 'drewj001', 'pedrd001', 'youkk001', 'ortid001', 'bay-j001', 'ellsj001', 'varij001', 'kotsm001', 'green001', 'tscht901', 'davib902', 'nelsj901', 'carlm901', 'wedge001', 'guilo001', 'sippt001', 'richc002', 'woodk002', 'shopk001', 'huffd001', 'richc002', 'cabra002', 'sizeg001', 'martv001', 'choos001', 'peraj001', 'garkr001', 'carrj001', 'franb001', 'shopk001', 'podss001', 'ramia003', 'dye-j001','thomj002', 'konep001', 'piera001', 'nix-j001', 'getzc001', 'beckg001', 'timmt901', 'wegnm901', 'kellj901', 'barrs901', 'giraj001', 'gardr001', 'albaj001', 'lirif001', 'rivem002', 'ransc001', 'aceva001', 'lirif001', 'jeted001', 'swisn001', 'teixm001', 'rodra001', 'posaj001', 'canor001', 'cabrm002', 'ransc001', 'gardb001', 'spand001', 'tolbm001', 'mauej001', 'mornj001', 'kubej002', 'cuddm001', 'buscb001', 'redmm001', 'puntn001', 'holbs901', 'iassd901', 'relic901', 'vanol901', 'washr001', 'wakad001', 'hernf002', 'wilsc004', 'aardd001', 'gutif001', 'huntt002', 'hernf002', 'kinsi001', 'younm003', 'hamij003', 'jonea002', 'blalh001', 'byrdm001', 'murpd005', 'saltj001', 'andre001', 'suzui001', 'branr001', 'lopej003', 'grifk002', 'gutif001', 'langr002', 'woodc001', 'johnr009', 'ceder002', 'welkt901', 'reynj901', 'hoyej901', 'welkb901', 'gastc101', 'maddj801', 'pricd001', 'hallr001', 'wheed001', 'penac001', 'hallr001', 'pricd001', 'bautj002', 'hilla001', 'linda001', 'millk005', 'wellv001', 'riosa002', 'overl001', 'barar001', 'mcdoj003', 'uptob001', 'crawc002', 'longe001', 'penac001', 'zobrb001', 'burrp001', 'grosg002', 'bartj001', 'hernm002']
participants_2007_5_2 = ['drakr901', 'rapue901', 'hicke901', 'westj901', 'manuc101', 'cox-b103', 'paroc001', 'garcf002', 'sorir001', 'harrw001', 'garcf002', 'jamec002', 'rollj001', 'rowaa001', 'utlec001', 'howar001', 'burrp001', 'helmw001', 'wertj001', 'barar001', 'garcf002', 'johnk003', 'rente001', 'jonec004', 'jonea002', 'thors001', 'franj004', 'saltj001', 'harrw001', 'jamec002', 'tscht901', 'joycj901', 'nelsj901', 'wolfj901', 'narrj001', 'garnp001', 'oswar001', 'lohsk001', 'wheed001', 'pench001', 'lohsk001', 'oswar001', 'freer001', 'hatts001', 'philb001', 'grifk002', 'gonza002', 'dunna001', 'hamij003', 'valej004', 'lohsk001', 'biggc001', 'pench001', 'berkl001', 'lee-c001', 'lorem001', 'scotl001', 'evera001', 'ausmb001', 'oswar001', 'reynj901', 'guccc901', 'cedeg901', 'barkl901', 'melvb001', 'littg801', 'hendm001', 'david002', 'saitt001', 'pierj002', 'david002', 'hendm001', 'younc004', 'jackc002', 'hudso001', 'byrne001', 'quenc001', 'drews001', 'snydc002', 'bardb001', 'david002', 'furcr001', 'pierj002', 'garcn001', 'kentj001', 'martr004', 'betew001', 'ethia001', 'clarb003', 'hendm001', 'scotd901', 'emmep901', 'iassd901', 'kulpr901', 'larut101', 'yoste001', 'villc001', 'reyea002', 'hartc001', 'reyea002', 'capuc001', 'tagus001', 'duncc002', 'pujoa001', 'roles001', 'spies001', 'benng001', 'milea001', 'ecksd001', 'reyea002', 'weekr001', 'hardj003', 'fielp001', 'hallb001', 'jenkg001', 'hartc001', 'milld002', 'graft001', 'capuc001', 'nauep901', 'gormb901', 'davig901', 'everm901', 'gonzf801', 'randw001', 'pereo002', 'sanca004', 'wagnb001', 'reyej001', 'sanca004', 'pereo002', 'ramih003', 'uggld001', 'cabrm001', 'willj004', 'boona001', 'rossc001', 'borcj001', 'tream001', 'sanca004', 'reyej001', 'chave002', 'beltc001', 'delgc001', 'wrigd002', 'grees001', 'castr002', 'gotar001', 'pereo002', 'hudsm901', 'barrt901', 'monte901', 'millb901', 'pinil001', 'tracj101', 'marqj001', 'sneli001', 'soria001', 'marqj001', 'sneli001', 'soria001', 'therr001','lee-d002', 'ramia001', 'floyc001', 'barrm003', 'jonej003', 'iztuc001', 'marqj001', 'duffc001', 'wilsj002', 'sancf001', 'bay-j001', 'laroa001', 'doumr001', 'bautj002', 'paulr001', 'sneli001', 'culbf901', 'darlg901', 'fostm901', 'schrp901', 'actam801', 'blacb001', 'brocd001', 'chicm001', 'kouzk001', 'chicm001', 'hensc002', 'lopef001', 'bellr002', 'zimmr001', 'churr001', 'keara001', 'schnb001', 'fickr001', 'castk001', 'chicm001', 'gilem001', 'cruzj004', 'gileb002', 'gonza003', 'greek002', 'bardj001', 'camem001', 'kouzk001', 'hensc002', 'hoyej901', 'reilm901', 'kellj901', 'coope901', 'hurdc001', 'bochb002', 'hennb001', 'franj003', 'bondb001', 'franj003', 'zitob001', 'tavew001', 'tulot001', 'hollm001', 'heltt001', 'atkig001', 'hawpb001', 'iannc001', 'carrj001', 'franj003', 'robed001', 'winnr001', 'aurir001', 'bondb001', 'durhr001', 'molib001', 'felip001', 'niekl001', 'zitob001', 'vanol901', 'gibsg901', 'hallt901', 'relic901', 'gereb001', 'frant001', 'beckj002', 'marsj001', 'timlm001', 'lugoj001', 'gaudc001', 'beckj002', 'stews002', 'ellim001', 'chave001', 'piazm001', 'johnd004', 'crosb002', 'putnd001', 'kendj001', 'langr002', 'lugoj001', 'youkk001', 'ortid001', 'ramim002', 'drewj001', 'lowem001', 'varij001', 'crisc001', 'coraa001', 'holbs901', 'wendh902', 'marsr901', 'davib902', 'gibbj001', 'wedge001', 'mastt001', 'marcs001', 'hafnt001', 'zambv001', 'westj001', 'riosa002', 'linda001', 'wellv001', 'thomf001', 'overl001', 'glaut001', 'hilla001', 'clayr001', 'fasas001', 'sizeg001', 'delld001', 'hafnt001', 'martv001', 'nixot001', 'garkr001', 'peraj001', 'blakc001', 'barfj003', 'muchm901', 'welkb901', 'bellw901', 'diazl901', 'perls101', 'leylj801', 'roben001', 'tracs001', 'jonet003', 'monrc001', 'tracs001', 'roben001', 'robeb003', 'paytj001', 'tejam001', 'hernr002', 'moram002', 'millk005', 'markn001', 'gomec001', 'pattc001', 'granc001', 'polap001', 'shefg001', 'ordom001', 'rodri001', 'cases001', 'monrc001', 'ingeb001', 'infao001', 'mcclt901', 'poncl901', 'mealj901', 'drecb901', 'sciom001', 'bellb001', 'delaj001', 'sante001', 'sorij001', 'germe001', 'sante001', 'delaj001', 'mattg002', 'willr004', 'cabro001', 'guerv001', 'quinr002', 'hills002', 'aybae001', 'napom001', 'figgc001', 'dejed001', 'germe001', 'teahm001', 'sandr002', 'gloar001', 'gorda001', 'butlb003', 'penat002', 'laruj001', 'reedr901', 'meric901', 'marqa901', 'timmt901', 'guilo001', 'hargm001', 'batim001', 'dankj001', 'putzj001', 'betay001', 'dankj001', 'batim001', 'erstd001', 'iguct001', 'piera001', 'konep001', 'dye-j001', 'mackr001', 'credj001', 'sweer001', 'uribj002', 'suzui001', 'belta001', 'vidrj001', 'ibanr001', 'sexsr001', 'guilj001', 'johjk001', 'betay001', 'lopej003', 'younl901', 'herna901', 'laynj901', 'carlm901', 'gardr001', 'maddj801', 'reyea001', 'guerm001', 'navad001', 'bonsb001', 'seo-j001','castl001', 'puntn001', 'mauej001', 'mornj001', 'huntt001', 'kubej002', 'cirij001', 'tynej001', 'bartj001', 'baldr001', 'dukee001', 'crawc002', 'wiggt001', 'yound003', 'uptob001', 'penac001', 'harrb001', 'paulj001']
listOfGames_2012_5_2 = ()
class TestResearcher(unittest.TestCase):
    
    def setUp(self):
        setup()
        self.maxDiff = None
        
    def tearDown(self):
        teardown()
    
    # #@unittest.skip("Too long")
    #@unittest.skip("Not Focus")
    def test_did_get_hit(self):
        # Edwin Jackon test
        self.assertFalse(R.did_get_hit(date(2012, 5, 2), p1))

        # Jose Reyes Tests (and one Albert Pujols)
        self.assertTrue(R.did_get_hit(date(2012, 6, 16), p2))
        self.assertTrue(R.did_get_hit(date(2005, 4, 4), p2))
        self.assertTrue(R.did_get_hit(date(2003, 7, 12), p2))
        self.assertFalse(R.did_get_hit(date(2012, 6, 15), p2))
        self.assertFalse(R.did_get_hit(date(2008, 9, 21), p2))

        # Alfonso Soriano Tests
        self.assertTrue(R.did_get_hit(date(2003, 3, 31), p3))
        self.assertTrue(R.did_get_hit(date(2009, 5, 12), p3))
        self.assertFalse(R.did_get_hit(date(2001, 9, 4), p3))
        self.assertFalse(R.did_get_hit(date(2007, 7, 20), p3))
        self.assertFalse(R.did_get_hit(date(2004, 9, 16), p3))

        # Jorge Posada tests
        self.assertTrue(R.did_get_hit(date(2004, 8, 17), p4))
        self.assertTrue(R.did_get_hit(date(2010, 7, 11), p4))
        self.assertFalse(R.did_get_hit(date(1997, 5, 23), p4))
        self.assertFalse(R.did_get_hit(date(2000, 4, 30), p4))

        # Manny Ramirez tests (traded in 2008. This test checks to see
        #   if did_get_hit works for players in a year they are traded)
        self.assertTrue(R.did_get_hit(date(1994, 7, 26), p5))
        self.assertTrue(R.did_get_hit(date(2008, 5, 22), p5))
        self.assertTrue(R.did_get_hit(date(2008, 8, 1), p5))
        self.assertFalse(R.did_get_hit(date(1995, 6, 30), p5))
        self.assertFalse(R.did_get_hit(date(2008, 7, 29), p5))
        self.assertFalse(R.did_get_hit(date(2008, 8, 31), p5))

        ## Larry Jones, from Player, test. Tests to see if it works even if
        ## the player has a nickname (Goes by Chipper instead of Larry)
        pL = Player('jonesch06', 2003)
        self.assertTrue(R.did_get_hit(date(2003, 4, 19), pL))
        self.assertFalse(R.did_get_hit(date(2003, 8, 28), pL))

        # Test Miguel Cabrera, Asdrubal Cabrera, Delmon Young, Michael Young.
        # Checks for proper answer when the functional line of the boxscore
        # has two players with the same last name
        MC1 = Player("Miguel", "Cabrera", 2012)
        MC2 = Player("Asdrubal", "Cabrera", 2012)
        dateMC = date(2012, 9, 5)
        self.assertTrue(R.did_get_hit(dateMC, MC1))
        self.assertFalse(R.did_get_hit(dateMC, MC2))

        MY1 = Player("Michael", "Young", 2012)
        MY2 = Player("Delmon", "Young", 2012)
        dateMY = date(2012, 6, 26)
        self.assertTrue(R.did_get_hit(dateMY, MY1))
        self.assertFalse(R.did_get_hit(dateMY, MY2))

        ## Double Header tests (its a hit iff player got a hit in first game)
        self.assertFalse(R.did_get_hit(date(1996, 9, 25), p4)) # T1, H2
        self.assertFalse(R.did_get_hit(date(2008, 9, 7), p2)) # T1, T2
        self.assertTrue(R.did_get_hit(date(2007, 7, 28), p2)) # H1, T2
        self.assertTrue(R.did_get_hit(date(2006, 6, 3), p2)) # H1, H2

        # Lance Berkman tests
        Lance = Player("Lance", "Berkman", 2008)
        self.assertTrue(R.did_get_hit(date(2009, 7, 9), Lance))

    @unittest.skip("Buffers have been thoroughly tested")
    def test_boxscore_buffer(self):
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

    #@unittest.skip("Not Focus")
    def test_get_hit_info(self):
        d1 = date(2012, 4, 15)
        d2 = date(2001, 7, 18)
        d3 = date(2010, 4, 16)
        d4 = date(2012, 7, 3)
        sGD2012 = R.get_sus_games_dict(2012) # assume works
        sGD2001 = R.get_sus_games_dict(2001) # assume works
        sGD2010 = R.get_sus_games_dict(2010) # assume works

        ## Case 1 : (True, None); player got a hit on date d1
        Jose = Player("Jose", "Altuve", 2012)
        self.assertEqual(R.get_hit_info(d1, Jose, sGD2012), (True, None))

        ## Case 2: (False, None); player did not get a hit on date date
        Will = Player("Will", "Venable", 2012)
        self.assertEqual(R.get_hit_info(d4, Will, sGD2012), (False, None))

        ## Case 3: ('pass', 'Suspended, Invalid'); player played in a suspended, invalid game
        Mark = Player("Mark", "Grace", 2001)
        self.assertEqual(R.get_hit_info(d2, Mark, sGD2001), ('pass', 'Suspended-Invalid.'))

        ## Case 4: (True, 'Suspended, Valid'); player got a hit in a suspended, valid game
        Ben = Player("Ben", "Zobrist", 2010)
        self.assertEqual(R.get_hit_info(d3, Ben, sGD2010), (True, 'Suspended-Valid.'))

        ## Case 5 : (False, 'Suspended, Valid'); player did not get a hit in a suspended, valid game
        Marco = Player("Marco", "Scutaro", 2010)
        self.assertEqual(R.get_hit_info(d3, Marco, sGD2010), (False, 'Suspended-Valid.'))

        ## Case 6: Get the player hit info from the playerInfoBuffer
        self.assertEqual(R.get_hit_info(d3, Ben, sGD2010), (True, 'Suspended-Valid.'))
        self.assertEqual(R.get_hit_info(d3, Marco, sGD2010), (False, 'Suspended-Valid.'))

    @unittest.skip("We get our hit info from cresearcher now")
    def test_player_info_buffer(self):
        d1 = date(2012, 4, 15)
        d2 = date(2001, 7, 18)
        d3 = date(2010, 4, 16)
        sGD2012 = R.get_sus_games_dict(2012) # assume works
        sGD2001 = R.get_sus_games_dict(2001) # assume works
        sGD2010 = R.get_sus_games_dict(2010) # assume works
        Ben = Player("Ben", "Zobrist", 2010)
        Jose = Player("Jose", "Altuve", 2012)
        Mark = Player("Mark", "Grace", 2001)
        Sammy = Player("Sammy", "Sosa", 2001)
        Marco = Player("Marco", "Scutaro", 2010)

        ## CHECK 1: Buffer updates current date (buffer slot 0)
        R.get_hit_info(d3, Ben, sGD2010)
        self.assertEqual(R.playerInfoBuffer[0], d3)
        R.get_hit_info(d1, Jose, sGD2012)
        self.assertEqual(R.playerInfoBuffer[0], d1)

        ## CHECK 2: If a player is on buffer, hit info is returned from buffer
            # artificially extend the player info buffer
        R.playerInfoBuffer[1].append((Ben, False, "oogly boogly")) 
            # Check that Jose Altuves hit info on d1 is returned from buffer
        R.playerUsedBuffer = False
        self.assertFalse(R.playerUsedBuffer)
        self.assertEqual(R.get_hit_info(d1, Jose, sGD2012), (True, None))
        self.assertTrue(R.playerUsedBuffer)
             # Check that Ben Zobrist's bogus hit info on d1 is returned from buffer
        R.playerUsedBuffer = False
        self.assertFalse(R.playerUsedBuffer)
        self.assertEqual(R.get_hit_info(d1, Ben, sGD2012), (False, "oogly boogly"))
        self.assertTrue(R.playerUsedBuffer)

        ## CHECK 3: If player NOT on buffer, hit info returned normally
           ## CHECK 3.1: Empty Buffer
        R.playerInfoBuffer = [d1, []] # reset the buffer
        R.playerUsedBuffer = False # rest buffer use indicator
        self.assertFalse(R.playerUsedBuffer)
        self.assertEqual(R.get_hit_info(d2, Mark, sGD2001), ('pass', 'Suspended-Invalid.'))
        self.assertFalse(R.playerUsedBuffer) # buffer use indicator should still be false
           ## CHECK 3.2: Nonempty buffer, on same date as previous hit info lookup
        self.assertEqual(R.get_hit_info(d2, Sammy, sGD2012), (False, None))
        self.assertFalse(R.playerUsedBuffer) # buffer use indicator should still be false

        ## Check 4: If date on buffer does not match current date, buffer is updated
        self.assertEqual(R.playerInfoBuffer, # should be d2 after Check 3
            [d2, [(Mark, 'pass', 'Suspended-Invalid.'), (Sammy, False, None)]]) 
        R.get_hit_info(d1, Jose, sGD2012)
        self.assertEqual(R.playerInfoBuffer, # should now be d1
            [d1, [(Jose, True, None)]]) 

        ## Check 5: If player's hit info obtained normally, his hit info
        ## is appended to buffer
            ## Check 5.1: New Date
        self.assertEqual(R.playerInfoBuffer, # buffer on d1 with Jose
            [d1, [(Jose, True, None)]]) 
        self.assertEqual(R.get_hit_info(d3, Marco, sGD2010), (False, 'Suspended-Valid.'))
        self.assertEqual(R.playerInfoBuffer, # buffer on d3 with Marco
            [d3, [(Marco, False, 'Suspended-Valid.')]])
            ## Check 5.2 Same Date
        self.assertEqual(R.get_hit_info(d3, Ben, sGD2010), (True, 'Suspended-Valid.'))
        self.assertEqual(R.playerInfoBuffer, # buffer on d3 with Marco and Ben
            [d3, [(Marco, False, 'Suspended-Valid.'), (Ben, True, 'Suspended-Valid.')]])

    #@unittest.skip("Not Focus")
    def test_get_batters_set(self):
        self.assertTrue(
            R._Researcher__get_batters_set(date(2011,9,4)).issubset(
            set(participants_2011_9_4)))
        self.assertTrue(
            R._Researcher__get_batters_set(date(2012,3,28)).issubset(
            set(participants_2012_3_28)))

        # # # Given a suspended game s1 that was started on date d1 and completed on
        # # # date d2, get_batters_set(d2) should NOT return players from d1
        self.assertTrue(
            R._Researcher__get_batters_set(date(2009, 7, 9)).issubset(
            set(participants_2009_7_9))) # May 5th HOU #@ WAS susp game completed on July 9th
        self.assertTrue(
            R._Researcher__get_batters_set(date(2007, 5, 2)).issubset(
            set(participants_2007_5_2)))# May 1st CHN #@ PIT suspended game completed on May 2

    @unittest.skip("Buffer thoroughly tested")
    def test_get_batters_set_buffer(self):
        # Check 1: if its not on the buffer, you get the right thing
        R.batterSetBuffer = [None, set({})]
        self.assertTrue(
            R._Researcher__get_batters_set(date(2011,9,4)).issubset(
            set(participants_2011_9_4)))

        # Check 2: if its on the buffer, you go get it from the buffer
        self.assertFalse(R.psUsedBuffer)
        self.assertTrue(
          R._Researcher__get_batters_set(date(2011,9,4)).issubset(
          set(participants_2011_9_4)))
        self.assertTrue(R.psUsedBuffer)
    #@unittest.skip("Not Focus")
    def test_find_home_team(self):
        Troy = Player("Troy", "Tulowitzki", 2010)
        self.assertEqual(R.find_home_team(date(2011, 8, 3), p1), "MIL")
        ## tests that the function works when used on consecutive days
        ## and on the second day the relevant game is the FIRST such game
        ## listed in the gamelog on the date. Why? To test that the optimizations
        ## in __get_list_of_games didn't screw everything up
        self.assertEqual(R.find_home_team(date(2011, 8, 4), Troy), "COL")

      # bunch of random tests
        self.assertEqual(R.find_home_team(date(2012, 5, 2), p1), "WAS")
        self.assertEqual(R.find_home_team(date(2012, 6, 15), p2), "TBA")
        self.assertEqual(R.find_home_team(date(2012, 9, 21), p2), "NYN")

    def test_list_of_games(self):
        #closing day
        listOfGames_2012_10_3 = (['20121003', '0', 'Wed', 'CHA', 'AL', '162', 'CLE', 'AL', '162', '9', '0', '54', 'N', '', '', '', 'CLE08', '18093', '170', '020140002', '000000000', '41', '16', '2', '0', '5', '9', '0', '0', '0', '5', '0', '7', '1', '0', '3', '0', '10', '3', '0', '0', '0', '0', '27', '7', '0', '0', '1', '0', '31', '5', '1', '0', '0', '0', '0', '0', '0', '2', '0', '9', '0', '0', '1', '0', '6', '6', '5', '5', '1', '0', '27', '13', '2', '0', '3', '0', 'everm901', 'Mike Everitt', 'diazl901', 'Laz Diaz', 'welkt901', 'Tim Welke', 'schrp901', 'Paul Schrieber', '', '(none)', '', '(none)', 'ventr001', 'Robin Ventura', 'aloms001', 'Sandy Alomar', 'floyg001', 'Gavin Floyd', 'huffd001', 'David Huff', '', '(none)', 'johnd004', 'Dan Johnson', 'floyg001', 'Gavin Floyd', 'huffd001', 'David Huff', 'hudso001', 'Orlando Hudson', '4', 'wised001', 'Dewayne Wise', '9', 'konep001', 'Paul Konerko', '10', 'vicid001', 'Dayan Viciedo', '7', 'johnd004', 'Dan Johnson', '3', 'lopej003', 'Jose Lopez', '5', 'gimeh001', 'Hector Gimenez', '2', 'dankj002', 'Jordan Danks', '8', 'olmer001', 'Ray Olmedo', '6', 'choos001', 'Shin-Soo Choo', '9', 'kipnj001', 'Jason Kipnis', '4', 'chisl001', 'Lonnie Chisenhall', '5', 'canzr001', 'Russ Canzler', '7', 'hafnt001', 'Travis Hafner', '10', 'phelc001', 'Cord Phelps', '6', 'hannj001', 'Jack Hannahan', '3', 'marsl001', 'Lou Marson', '2', 'donaj002', 'Jason Donald', '8', '', 'Y\n'], ['20121003', '0', 'Wed', 'DET', 'AL', '162', 'KCA', 'AL', '162', '1', '0', '54', 'N', '', '', '', 'KAN06', '30383', '179', '000010000', '000000000', '30', '7', '2', '0', '0', '1', '1', '0', '0', '4', '0', '8', '2', '0', '3', '0', '7', '4', '0', '0', '0', '0', '27', '9', '0', '0', '1', '0', '31', '6', '0', '0', '0', '0', '0', '0', '0', '7', '0', '6', '1', '0', '1', '0', '11', '4', '1', '1', '0', '0', '27', '13', '0', '1', '3', '0', 'wintm901', 'Mike Winters', 'wegnm901', 'Mark Wegner', 'holbs901', 'Sam Holbrook', 'knigb901', 'Brian Knight', '', '(none)', '', '(none)', 'leylj801', 'Jim Leyland', 'yoste001', 'Ned Yost', 'martl003', 'Luis Marte', 'mendl001', 'Luis Mendoza', 'putkl001', 'Luke Putkonen', 'jacka001', 'Austin Jackson', 'schem001', 'Max Scherzer', 'mendl001', 'Luis Mendoza', 'jacka001', 'Austin Jackson', '8', 'berrq001', 'Quintin Berry', '7', 'cabrm001', 'Miguel Cabrera', '5', 'fielp001', 'Prince Fielder', '10', 'avila001', 'Alex Avila', '2', 'peraj001', 'Jhonny Peralta', '6', 'dirka001', 'Andy Dirks', '9', 'infao001', 'Omar Infante', '4', 'kelld001', 'Don Kelly', '3', 'dysoj001', 'Jarrod Dyson', '8', 'escoa003', 'Alcides Escobar', '6', 'gorda001', 'Alex Gordon', '7', 'butlb003', 'Billy Butler', '3', 'franj004', 'Jeff Francoeur', '9', 'penab002', 'Brayan Pena', '10', 'moora001', 'Adam Moore', '2', 'giavj001', 'Johnny Giavotella', '4', 'falui001', 'Irving Falu', '5', '', 'Y\n'], ['20121003', '0', 'Wed', 'BOS', 'AL', '162', 'NYA', 'AL', '162', '2', '14', '51', 'N', '', '', '', 'NYC21', '47393', '203', '100000100', '03202250x', '33', '8', '3', '0', '0', '2', '0', '0', '0', '2', '0', '9', '1', '1', '1', '0', '6', '7', '14', '14', '0', '0', '24', '7', '0', '0', '1', '0', '37', '15', '3', '0', '4', '14', '0', '1', '1', '7', '0', '5', '1', '0', '1', '0', '8', '4', '2', '2', '0', '0', '27', '10', '0', '0', '1', '0', 'buckc901', 'CB Bucknor', 'scotd901', 'Dale Scott', 'iassd901', 'Dan Iassogna', 'millb901', 'Bill Miller', '', '(none)', '', '(none)', 'valeb102', 'Bobby Valentine', 'giraj001', 'Joe Girardi', 'kuroh001', 'Hiroki Kuroda', 'matsd001', 'Daisuke Matsuzaka', '', '(none)', 'granc001', 'Curtis Granderson', 'matsd001', 'Daisuke Matsuzaka', 'kuroh001', 'Hiroki Kuroda', 'ellsj001', 'Jacoby Ellsbury', '8', 'pedrd001', 'Dustin Pedroia', '4', 'navad002', 'Daniel Nava', '7', 'rossc001', 'Cody Ross', '9', 'lonej001', 'James Loney', '3', 'saltj001', 'Jarrod Saltalamacchia', '2', 'lavar001', 'Ryan Lavarnway', '10', 'cirip001', 'Pedro Ciriaco', '5', 'iglej001', 'Jose Iglesias', '6', 'jeted001', 'Derek Jeter', '6', 'suzui001', 'Ichiro Suzuki', '7', 'rodra001', 'Alex Rodriguez', '5', 'canor001', 'Robinson Cano', '4', 'swisn001', 'Nick Swisher', '9', 'teixm001', 'Mark Teixeira', '3', 'granc001', 'Curtis Granderson', '8', 'ibanr001', 'Raul Ibanez', '10', 'martr004', 'Russell Martin', '2', '', 'Y\n'], ['20121003', '0', 'Wed', 'TEX', 'AL', '162', 'OAK', 'AL', '162', '5', '12', '51', 'D', '', '', '', 'OAK01', '36067', '196', '005000000', '10061004x', '39', '11', '3', '0', '0', '5', '0', '0', '0', '3', '0', '8', '0', '0', '0', '0', '10', '5', '8', '8', '1', '0', '24', '6', '3', '0', '0', '0', '37', '11', '3', '0', '1', '9', '0', '0', '0', '5', '0', '6', '0', '0', '0', '0', '6', '6', '4', '4', '0', '0', '27', '9', '1', '0', '0', '0', 'cedeg901', 'Gary Cederstrom', 'johna901', 'Adrian Johnson', 'barkl901', 'Lance Barksdale', 'culbf901', 'Fieldin Culbreth', '', '(none)', '', '(none)', 'washr001', 'Ron Washington', 'melvb001', 'Bob Melvin', 'scrie001', 'Evan Scribner', 'holld003', 'Derek Holland', '', '(none)', '', '(none)', 'dempr002', 'Ryan Dempster', 'grifa002', 'A.J. Griffin', 'kinsi001', 'Ian Kinsler', '4', 'andre001', 'Elvis Andrus', '6', 'hamij003', 'Josh Hamilton', '8', 'belta001', 'Adrian Beltre', '10', 'cruzn002', 'Nelson Cruz', '9', 'younm003', 'Michael Young', '5', 'murpd005', 'David Murphy', '7', 'napom001', 'Mike Napoli', '3', 'sotog001', 'Geovany Soto', '2', 'crisc001', 'Coco Crisp', '8', 'drews001', 'Stephen Drew', '6', 'cespy001', 'Yoenis Cespedes', '7', 'mossb001', 'Brandon Moss', '3', 'reddj001', 'Josh Reddick', '9', 'donaj001', 'Josh Donaldson', '5', 'smits002', 'Seth Smith', '10', 'kottg001', 'George Kottaras', '2', 'pennc001', 'Cliff Pennington', '4', '', 'Y\n'], ['20121003', '0', 'Wed', 'ANA', 'AL', '162', 'SEA', 'AL', '162', '0', '12', '51', 'D', '', '', '', 'SEA03', '15614', '176', '000000000', '20200260x', '31', '7', '2', '0', '0', '0', '0', '0', '1', '1', '0', '2', '1', '1', '1', '0', '6', '6', '12', '12', '1', '0', '24', '9', '2', '0', '0', '0', '36', '11', '3', '0', '1', '11', '0', '0', '1', '6', '0', '6', '0', '0', '0', '0', '7', '2', '0', '0', '0', '0', '27', '8', '0', '0', '2', '0', 'davib902', 'Bob Davidson', 'gormb901', 'Brian Gorman', 'randt901', 'Tony Randazzo', 'ticht901', 'Todd Tichenor', '', '(none)', '', '(none)', 'sciom001', 'Mike Scioscia', 'wedge001', 'Eric Wedge', 'beavb001', 'Blake Beavan', 'weavj003', 'Jered Weaver', '', '(none)', 'seagk001', 'Kyle Seager', 'weavj003', 'Jered Weaver', 'beavb001', 'Blake Beavan', 'troum001', 'Mike Trout', '8', 'huntt001', 'Torii Hunter', '9', 'pujoa001', 'Albert Pujols', '10', 'morak001', 'Kendrys Morales', '3', 'calla001', 'Alberto Callaspo', '5', 'trumm001', 'Mark Trumbo', '7', 'kendh001', 'Howie Kendrick', '4', 'iztum001', 'Maicer Izturis', '6', 'iannc001', 'Chris Iannetta', '2', 'ackld001', 'Dustin Ackley', '4', 'wellc001', 'Casper Wells', '9', 'seagk001', 'Kyle Seager', '5', 'jasoj001', 'John Jaso', '10', 'smoaj001', 'Justin Smoak', '3', 'montj003', 'Jesus Montero', '2', 'saunm001', 'Michael Saunders', '8', 'robit001', 'Trayvon Robinson', '7', 'triuc001', 'Carlos Triunfel', '6', '', 'Y\n'], ['20121003', '0', 'Wed', 'BAL', 'AL', '162', 'TBA', 'AL', '162', '1', '4', '51', 'N', '', '', '', 'STP01', '17909', '163', '000000001', '10020100x', '30', '3', '1', '0', '0', '1', '0', '1', '0', '2', '0', '10', '0', '0', '0', '0', '5', '5', '4', '4', '0', '0', '24', '4', '0', '0', '0', '0', '30', '6', '0', '0', '4', '4', '0', '0', '0', '0', '0', '8', '0', '0', '0', '0', '2', '5', '1', '1', '1', '0', '27', '8', '0', '0', '0', '0', 'barrt901', 'Ted Barrett', 'carlm901', 'Mark Carlson', 'herna901', 'Angel Hernandez', 'hicke901', 'Ed Hickox', '', '(none)', '', '(none)', 'showb801', 'Buck Showalter', 'maddj801', 'Joe Maddon', 'hellj001', 'Jeremy Hellickson', 'tillc001', 'Chris Tillman', 'rodnf001', 'Fernando Rodney', 'longe001', 'Evan Longoria', 'tillc001', 'Chris Tillman', 'hellj001', 'Jeremy Hellickson', 'mclon001', 'Nate McLouth', '7', 'hardj003', 'J.J. Hardy', '6', 'davic003', 'Chris Davis', '9', 'jonea003', 'Adam Jones', '8', 'wietm001', 'Matt Wieters', '2', 'thomj002', 'Jim Thome', '10', 'reynm001', 'Mark Reynolds', '3', 'flahr001', 'Ryan Flaherty', '4', 'machm001', 'Manny Machado', '5', 'uptob001', 'B.J. Upton', '8', 'zobrb001', 'Ben Zobrist', '6', 'longe001', 'Evan Longoria', '5', 'joycm001', 'Matthew Joyce', '9', 'rober002', 'Ryan Roberts', '4', 'penac001', 'Carlos Pena', '3', 'fulds001', 'Sam Fuld', '7', 'vogts001', 'Stephen Vogt', '10', 'gimec001', 'Chris Gimenez', '2', '', 'Y\n'], ['20121003', '0', 'Wed', 'MIN', 'AL', '162', 'TOR', 'AL', '162', '1', '2', '51', 'N', '', '', '', 'TOR02', '19769', '141', '000100000', '00200000x', '31', '4', '0', '0', '0', '1', '0', '0', '0', '3', '0', '11', '1', '0', '0', '0', '6', '3', '2', '2', '1', '0', '24', '11', '0', '0', '2', '0', '28', '6', '0', '1', '0', '2', '0', '0', '0', '1', '0', '6', '1', '0', '2', '0', '3', '2', '1', '1', '0', '0', '27', '7', '0', '0', '0', '0', 'basnt901', 'Toby Basner', 'mcclt901', 'Tim McClelland', 'hudsm901', 'Marvin Hudson', 'fagac901', 'Clint Fagan', '', '(none)', '', '(none)', 'gardr001', 'Ron Gardenhire', 'farrj001', 'John Farrell', 'morrb001', 'Brandon Morrow', 'diams001', 'Scott Diamond', 'lyonb003', 'Brandon Lyon', 'davir003', 'Rajai Davis', 'diams001', 'Scott Diamond', 'morrb001', 'Brandon Morrow', 'spand001', 'Denard Span', '8', 'reveb001', 'Ben Revere', '9', 'mauej001', 'Joe Mauer', '10', 'parmc001', 'Chris Parmelee', '3', 'plout001', 'Trevor Plouffe', '5', 'carsm001', 'Matt Carson', '7', 'escoe001', 'Eduardo Escobar', '4', 'buted001', 'Drew Butera', '2', 'florp001', 'Pedro Florimon', '6', 'davir003', 'Rajai Davis', '7', 'hecha001', 'Adeiny Hechavarria', '4', 'lawrb002', 'Brett Lawrie', '5', 'linda001', 'Adam Lind', '10', 'gomey001', 'Yan Gomes', '3', 'arenj001', 'J.P. Arencibia', '2', 'vizqo001', 'Omar Vizquel', '6', 'sierm001', 'Moises Sierra', '9', 'gosea001', 'Anthony Gose', '8', '', 'Y\n'], ['20121003', '0', 'Wed', 'COL', 'NL', '162', 'ARI', 'NL', '162', '2', '1', '54', 'D', '', '', '', 'PHO01', '24344', '196', '000200000', '001000000', '35', '10', '0', '0', '0', '1', '2', '0', '1', '0', '0', '12', '0', '1', '0', '0', '9', '7', '1', '1', '0', '0', '27', '11', '0', '1', '1', '0', '32', '7', '0', '0', '1', '1', '1', '0', '1', '4', '1', '5', '3', '0', '1', '0', '10', '3', '0', '0', '0', '0', '27', '6', '1', '0', '0', '0', 'rippm901', 'Mark Ripperger', 'barrs901', 'Scott Barry', 'darlg901', 'Gary Darling', 'mealj901', 'Jerry Meals', '', '(none)', '', '(none)', 'tracj101', 'Jim Tracy', 'gibsk001', 'Kirk Gibson', 'franj003', 'Jeff Francis', 'kenni001', 'Ian Kennedy', 'belim001', 'Matt Belisle', 'lemad001', 'DJ LeMahieu', 'franj003', 'Jeff Francis', 'kenni001', 'Ian Kennedy', 'rutlj001', 'Josh Rutledge', '4', 'blacc001', 'Charlie Blackmon', '7', 'pachj001', 'Jordan Pacheco', '3', 'rosaw001', 'Wilin Rosario', '2', 'colvt001', 'Tyler Colvin', '8', 'browa003', 'Andrew Brown', '9', 'lemad001', 'DJ LeMahieu', '5', 'herrj002', 'Jonathan Herrera', '6', 'franj003', 'Jeff Francis', '1', 'polla001', 'A.J. Pollock', '8', 'hilla001', 'Aaron Hill', '4', 'uptoj001', 'Justin Upton', '9', 'goldp001', 'Paul Goldschmidt', '3', 'montm001', 'Miguel Montero', '2', 'johnc003', 'Chris Johnson', '5', 'parrg001', 'Gerardo Parra', '7', 'mcdoj003', 'John McDonald', '6', 'kenni001', 'Ian Kennedy', '1', '', 'Y\n'], ['20121003', '0', 'Wed', 'HOU', 'NL', '162', 'CHN', 'NL', '162', '4', '5', '53', 'D', '', '', '', 'CHI11', '27606', '184', '100000030', '010300001', '31', '6', '1', '0', '1', '4', '0', '0', '0', '6', '0', '6', '0', '1', '2', '0', '6', '6', '5', '5', '0', '0', '26', '10', '1', '0', '1', '0', '32', '7', '0', '0', '1', '5', '0', '0', '0', '8', '0', '5', '2', '0', '1', '0', '9', '4', '3', '3', '0', '0', '27', '13', '1', '0', '2', '0', 'tumpj901', 'John Tumpane', 'wolfj901', 'Jim Wolf', 'kulpr901', 'Ron Kulpa', 'bellw901', 'Wally Bell', '', '(none)', '', '(none)', 'defrt801', 'Tony DeFrancesco', 'sveud001', 'Dale Sveum', 'marmc001', 'Carlos Marmol', 'ambrh001', 'Hector Ambriz', '', '(none)', 'lahab001', 'Bryan LaHair', 'gonze001', 'Edgar Gonzalez', 'woodt004', 'Travis Wood', 'greet004', 'Tyler Greene', '4', 'lowrj001', 'Jed Lowrie', '6', 'domim001', 'Matt Dominguez', '5', 'maxwj002', 'Justin Maxwell', '7', 'corpc001', 'Carlos Corporan', '2', 'barnb002', 'Brandon Barnes', '8', 'lairb001', 'Brandon Laird', '3', 'parej002', 'Jimmy Paredes', '9', 'gonze001', 'Edgar Gonzalez', '1', 'campt001', 'Tony Campana', '7', 'carda001', 'Adrian Cardenas', '4', 'casts001', 'Starlin Castro', '6', 'lahab001', 'Bryan LaHair', '3', 'sappd001', 'Dave Sappelt', '9', 'vittj001', 'Josh Vitters', '5', 'jackb002', 'Brett Jackson', '8', 'recka001', 'Anthony Recker', '2', 'woodt004', 'Travis Wood', '1', '', 'Y\n'], ['20121003', '0', 'Wed', 'SFN', 'NL', '162', 'LAN', 'NL', '162', '1', '5', '51', 'D', '', '', '', 'LOS03', '34014', '158', '000100000', '00001103x', '29', '3', '2', '0', '0', '1', '0', '0', '0', '4', '0', '10', '0', '1', '0', '0', '5', '4', '4', '4', '0', '0', '24', '6', '1', '0', '0', '0', '32', '8', '1', '0', '2', '5', '0', '0', '0', '1', '0', '8', '0', '0', '0', '0', '4', '2', '1', '1', '0', '0', '27', '12', '0', '0', '0', '0', 'vanol901', 'Larry Vanover', 'belld901', 'Dan Bellino', 'laynj901', 'Jerry Layne', 'emmep901', 'Paul Emmel', '', '(none)', '', '(none)', 'bochb002', 'Bruce Bochy', 'mattd001', 'Don Mattingly', 'kersc001', 'Clayton Kershaw', 'hensc002', 'Clay Hensley', '', '(none)', 'gonza003', 'Adrian Gonzalez', 'voger001', 'Ryan Vogelsong', 'kersc001', 'Clayton Kershaw', 'pagaa001', 'Angel Pagan', '8', 'scutm001', 'Marco Scutaro', '4', 'sandp001', 'Pablo Sandoval', '5', 'poseb001', 'Buster Posey', '2', 'pench001', 'Hunter Pence', '9', 'nadyx001', 'Xavier Nady', '7', 'beltb001', 'Brandon Belt', '3', 'ariaj001', 'Joaquin Arias', '6', 'voger001', 'Ryan Vogelsong', '1', 'ellim001', 'Mark Ellis', '4', 'ethia001', 'Andre Ethier', '9', 'kempm001', 'Matt Kemp', '8', 'gonza003', 'Adrian Gonzalez', '3', 'ramih003', 'Hanley Ramirez', '6', 'victs001', 'Shane Victorino', '7', 'cruzl001', 'Luis Cruz', '5', 'fedet001', 'Tim Federowicz', '2', 'kersc001', 'Clayton Kershaw', '1', '', 'Y\n'], ['20121003', '0', 'Wed', 'NYN', 'NL', '162', 'MIA', 'NL', '162', '4', '2', '54', 'D', '', '', '', 'MIA02', '27418', '158', '001201000', '000001010', '36', '10', '2', '1', '3', '4', '0', '0', '1', '1', '0', '7', '0', '0', '1', '0', '7', '4', '2', '2', '1', '0', '27', '12', '0', '1', '0', '0', '33', '7', '2', '0', '0', '1', '0', '0', '0', '4', '0', '8', '1', '0', '0', '0', '8', '4', '4', '4', '0', '0', '27', '7', '0', '0', '1', '0', 'fleta901', 'Andy Fletcher', 'carav901', 'Vic Carapazza', 'muchm901', 'Mike Muchlinski', 'drakr901', 'Rob Drake', '', '(none)', '', '(none)', 'collt801', 'Terry Collins', 'guilo001', 'Ozzie Guillen', 'hefnj001', 'Jeremy Hefner', 'koeht001', 'Tom Koehler', 'parnb001', 'Bobby Parnell', 'torra001', 'Andres Torres', 'hefnj001', 'Jeremy Hefner', 'koeht001', 'Tom Koehler', 'tejar001', 'Ruben Tejada', '6', 'murpd006', 'Dan Murphy', '4', 'wrigd002', 'David Wright', '5', 'davii001', 'Ike Davis', '3', 'hairs001', 'Scott Hairston', '9', 'dudal001', 'Lucas Duda', '7', 'shopk001', 'Kelly Shoppach', '2', 'torra001', 'Andres Torres', '8', 'hefnj001', 'Jeremy Hefner', '1', 'peteb001', 'Bryan Petersen', '7', 'herng001', 'Gorkys Hernandez', '8', 'reyej001', 'Jose Reyes', '6', 'stanm004', 'Giancarlo Stanton', '9', 'lee-c001', 'Carlos Lee', '3', 'solad001', 'Donovan Solano', '4', 'buckj001', 'John Buck', '2', 'velag002', 'Gil Velazquez', '5', 'koeht001', 'Tom Koehler', '1', '', 'Y\n'], ['20121003', '0', 'Wed', 'SDN', 'NL', '162', 'MIL', 'NL', '162', '7', '6', '54', 'N', '', '', '', 'MIL06', '34451', '178', '000122200', '114000000', '34', '9', '4', '1', '2', '6', '0', '1', '0', '4', '0', '6', '2', '0', '1', '0', '5', '7', '5', '5', '0', '0', '27', '8', '2', '0', '0', '0', '35', '7', '2', '0', '0', '6', '0', '0', '0', '2', '1', '6', '3', '0', '0', '0', '4', '6', '7', '7', '0', '0', '27', '11', '1', '0', '1', '0', 'hoyej901', 'James Hoye', 'joycj901', 'Jim Joyce', 'porta901', 'Alan Porter', 'reynj901', 'Jim Reynolds', '', '(none)', '', '(none)', 'blacb001', 'Buddy Black', 'roenr001', 'Ron Roenicke', 'laynt001', 'Tom Layne', 'hendj001', 'Jim Henderson', 'gregl001', 'Luke Gregerson', 'alony001', 'Yonder Alonso', 'werna001', 'Andrew Werner', 'stinj001', 'Josh Stinson', 'cabre001', 'Everth Cabrera', '6', 'venaw001', 'Will Venable', '9', 'headc001', 'Chase Headley', '5', 'grany001', 'Yasmani Grandal', '2', 'alony001', 'Yonder Alonso', '3', 'denoc001', 'Chris Denorfia', '7', 'maybc001', 'Cameron Maybin', '8', 'parra001', 'Andy Parrino', '4', 'werna001', 'Andrew Werner', '1', 'aokin001', 'Norichika Aoki', '9', 'weekr001', 'Rickie Weeks', '4', 'braur002', 'Ryan Braun', '7', 'ramia001', 'Aramis Ramirez', '5', 'lucrj001', 'Jonathan Lucroy', '2', 'gomec002', 'Carlos Gomez', '8', 'ishit001', 'Travis Ishikawa', '3', 'seguj002', 'Jean Segura', '6', 'stinj001', 'Josh Stinson', '1', '', 'Y\n'], ['20121003', '0', 'Wed', 'ATL', 'NL', '162', 'PIT', 'NL', '162', '4', '0', '54', 'D', '', '', '', 'PIT08', '20615', '165', '100102000', '000000000', '33', '10', '0', '0', '0', '4', '1', '1', '0', '2', '0', '9', '3', '0', '1', '0', '6', '8', '0', '0', '0', '0', '27', '12', '0', '0', '0', '0', '30', '4', '0', '0', '0', '0', '0', '0', '0', '0', '0', '11', '0', '0', '0', '0', '3', '5', '4', '4', '0', '0', '27', '12', '0', '0', '1', '0', 'blasc901', 'Cory Blaser', 'guccc901', 'Chris Guccione', 'nelsj901', 'Jeff Nelson', 'welkb901', 'Bill Welke', '', '(none)', '', '(none)', 'gonzf801', 'Fredi Gonzalez', 'hurdc001', 'Clint Hurdle', 'avill001', 'Luis Avilan', 'burna001', 'A.J. Burnett', '', '(none)', 'pradm001', 'Martin Prado', 'sheeb001', 'Ben Sheets', 'burna001', 'A.J. Burnett', 'bourm001', 'Michael Bourn', '8', 'pradm001', 'Martin Prado', '7', 'heywj001', 'Jason Heyward', '9', 'freef001', 'Freddie Freeman', '3', 'uggld001', 'Dan Uggla', '4', 'mccab002', 'Brian McCann', '2', 'franj005', 'Juan Francisco', '5', 'simma001', 'Andrelton Simmons', '6', 'sheeb001', 'Ben Sheets', '1', 'marts002', 'Starling Marte', '7', 'presa001', 'Alex Presley', '9', 'mccua001', 'Andrew McCutchen', '8', 'joneg002', 'Garrett Jones', '3', 'alvap001', 'Pedro Alvarez', '5', 'harrj002', 'Josh Harrison', '4', 'barmc001', 'Clint Barmes', '6', 'barar001', 'Rod Barajas', '2', 'burna001', 'A.J. Burnett', '1', '', 'Y\n'], ['20121003', '0', 'Wed', 'CIN', 'NL', '162', 'SLN', 'NL', '162', '0', '1', '51', 'N', '', '', '', 'STL10', '42509', '154', '000000000', '00000001x', '29', '3', '0', '0', '0', '0', '0', '0', '1', '2', '0', '10', '0', '1', '1', '0', '5', '6', '1', '1', '0', '0', '24', '4', '0', '0', '0', '0', '33', '9', '1', '0', '0', '1', '0', '0', '0', '1', '0', '11', '1', '0', '0', '0', '9', '5', '0', '0', '0', '0', '27', '8', '1', '0', '1', '0', 'marqa901', 'Alfonso Marquez', 'hallt901', 'Tom Hallion', 'onorb901', "Brian O'Nora", 'fairc901', 'Chad Fairchild', '', '(none)', '', '(none)', 'baked002', 'Dusty Baker', 'mathm001', 'Mike Matheny', 'martv002', 'Victor Marte', 'broxj001', 'Jonathan Broxton', 'mottj001', 'Jason Motte', 'carpm002', 'Matt Carpenter', 'bailh001', 'Homer Bailey', 'mills001', 'Shelby Miller', 'philb001', 'Brandon Phillips', '4', 'cozaz001', 'Zack Cozart', '6', 'vottj001', 'Joey Votto', '3', 'ludwr001', 'Ryan Ludwick', '7', 'brucj001', 'Jay Bruce', '9', 'roles001', 'Scott Rolen', '5', 'hanir001', 'Ryan Hanigan', '2', 'stubd001', 'Drew Stubbs', '8', 'bailh001', 'Homer Bailey', '1', 'chama002', 'Adron Chambers', '7', 'robis001', 'Shane Robinson', '8', 'schus001', 'Skip Schumaker', '9', 'carpm002', 'Matt Carpenter', '5', 'cruzt002', 'Tony Cruz', '2', 'andeb005', 'Bryan Anderson', '3', 'jackr005', 'Ryan Jackson', '4', 'kozmp001', 'Peter Kozma', '6', 'mills001', 'Shelby Miller', '1', '', 'Y\n'], ['20121003', '0', 'Wed', 'PHI', 'NL', '162', 'WAS', 'NL', '162', '1', '5', '51', 'D', '', '', '', 'WAS11', '37075', '180', '000100000', '00020102x', '32', '6', '4', '0', '0', '1', '0', '1', '0', '2', '0', '8', '0', '0', '0', '0', '7', '4', '5', '5', '0', '0', '24', '3', '0', '0', '0', '0', '35', '11', '3', '1', '3', '5', '0', '0', '0', '1', '0', '10', '0', '0', '0', '0', '7', '4', '1', '1', '0', '0', '27', '9', '0', '0', '0', '0', 'gibsg901', 'Greg Gibson', 'cuzzp901', 'Phil Cuzzi', 'davig901', 'Gerry Davis', 'gonzm901', 'Manny Gonzalez', '', '(none)', '', '(none)', 'manuc101', 'Charlie Manuel', 'johnd105', 'Davey Johnson', 'jacke001', 'Edwin Jackson', 'lee-c003', 'Cliff Lee', '', '(none)', 'moort002', 'Tyler Moore', 'lee-c003', 'Cliff Lee', 'jacke001', 'Edwin Jackson', 'pierj002', 'Juan Pierre', '7', 'frank001', 'Kevin Frandsen', '5', 'utlec001', 'Chase Utley', '4', 'ruizc001', 'Carlos Ruiz', '2', 'browd004', 'Domonic Brown', '9', 'ruf-d001', 'Darin Ruf', '3', 'schin001', 'Nate Schierholtz', '8', 'martm003', 'Michael Martinez', '6', 'lee-c003', 'Cliff Lee', '1', 'wertj001', 'Jayson Werth', '8', 'derom001', 'Mark DeRosa', '9', 'zimmr001', 'Ryan Zimmerman', '5', 'morsm001', 'Mike Morse', '7', 'moort002', 'Tyler Moore', '3', 'desmi001', 'Ian Desmond', '6', 'espid001', 'Danny Espinosa', '4', 'florj002', 'Jesus Flores', '2', 'jacke001', 'Edwin Jackson', '1', '', 'Y\n'])
        #opening day
        listOfGames_2011_3_31 = (['20110331', '0', 'Thu', 'MIL', 'NL', '1', 'CIN', 'NL', '1', '6', '7', '53', 'D', '', '', '', 'CIN09', '42398', '189', '310010100', '100100104', '35', '9', '2', '0', '3', '6', '0', '1', '0', '5', '2', '7', '1', '0', '0', '0', '8', '4', '7', '7', '0', '0', '26', '8', '0', '0', '0', '0', '35', '12', '1', '0', '3', '7', '2', '2', '0', '4', '0', '10', '0', '0', '0', '0', '10', '5', '6', '6', '1', '1', '27', '11', '1', '0', '0', '0', 'gormb901', 'Brian Gorman', 'vanol901', 'Larry Vanover', 'randt901', 'Tony Randazzo', 'belld901', 'Dan Bellino', '', '(none)', '', '(none)', 'roenr001', 'Ron Roenicke', 'baked002', 'Dusty Baker', 'ondrl001', 'Logan Ondrusek', 'axfoj001', 'John Axford', '', '(none)', 'hernr002', 'Ramon Hernandez', 'gally001', 'Yovani Gallardo', 'volqe001', 'Edinson Volquez', 'weekr001', 'Rickie Weeks', '4', 'gomec002', 'Carlos Gomez', '8', 'braur002', 'Ryan Braun', '7', 'fielp001', 'Prince Fielder', '3', 'mcgec001', 'Casey McGehee', '5', 'kotsm001', 'Mark Kotsay', '9', 'betay001', 'Yuniesky Betancourt', '6', 'nievw001', 'Wil Nieves', '2', 'gally001', 'Yovani Gallardo', '1', 'stubd001', 'Drew Stubbs', '8', 'philb001', 'Brandon Phillips', '4', 'vottj001', 'Joey Votto', '3', 'roles001', 'Scott Rolen', '5', 'brucj001', 'Jay Bruce', '9', 'gomej001', 'Jonny Gomes', '7', 'hernr002', 'Ramon Hernandez', '2', 'janip001', 'Paul Janish', '6', 'volqe001', 'Edinson Volquez', '1', '', 'Y\n'], ['20110331', '0', 'Thu', 'SFN', 'NL', '1', 'LAN', 'NL', '1', '1', '2', '51', 'N', '', '', '', 'LOS03', '56000', '170', '000000001', '00000101x', '32', '5', '0', '0', '1', '1', '0', '0', '0', '2', '0', '10', '0', '0', '1', '0', '6', '2', '1', '1', '0', '0', '24', '9', '3', '1', '0', '0', '30', '6', '1', '0', '0', '1', '0', '0', '1', '4', '1', '6', '1', '0', '0', '0', '9', '3', '1', '1', '0', '0', '27', '9', '1', '0', '1', '0', 'cedeg901', 'Gary Cederstrom', 'barkl901', 'Lance Barksdale', 'culbf901', 'Fieldin Culbreth', 'johna901', 'Adrian Johnson', '', '(none)', '', '(none)', 'bochb002', 'Bruce Bochy', 'mattd001', 'Don Mattingly', 'kersc001', 'Clayton Kershaw', 'linct001', 'Tim Lincecum', 'broxj001', 'Jonathan Broxton', '', '(none)', 'linct001', 'Tim Lincecum', 'kersc001', 'Clayton Kershaw', 'torra001', 'Andres Torres', '8', 'sancf001', 'Freddy Sanchez', '4', 'huffa001', 'Aubrey Huff', '9', 'poseb001', 'Buster Posey', '2', 'burrp001', 'Pat Burrell', '7', 'tejam001', 'Miguel Tejada', '6', 'beltb001', 'Brandon Belt', '3', 'sandp001', 'Pablo Sandoval', '5', 'linct001', 'Tim Lincecum', '1', 'furcr001', 'Rafael Furcal', '6', 'gwynt002', 'Tony Gwynn', '7', 'ethia001', 'Andre Ethier', '9', 'kempm001', 'Matt Kemp', '8', 'lonej001', 'James Loney', '3', 'uribj002', 'Juan Uribe', '5', 'barar001', 'Rod Barajas', '2', 'carrj001', 'Jamey Carroll', '4', 'kersc001', 'Clayton Kershaw', '1', '', 'Y\n'], ['20110331', '0', 'Thu', 'SDN', 'NL', '1', 'SLN', 'NL', '1', '5', '3', '66', 'D', '', '', '', 'STL10', '46368', '197', '00011000102', '10010001000', '39', '8', '2', '0', '1', '4', '0', '1', '2', '3', '0', '6', '1', '0', '1', '0', '7', '6', '3', '3', '0', '0', '33', '19', '0', '1', '4', '0', '40', '12', '0', '1', '1', '3', '1', '0', '0', '3', '0', '5', '0', '1', '4', '0', '8', '6', '4', '4', '0', '0', '33', '11', '1', '0', '1', '0', 'kellj901', 'Jeff Kellogg', 'coope901', 'Eric Cooper', 'carlm901', 'Mark Carlson', 'timmt901', 'Tim Timmons', '', '(none)', '', '(none)', 'blacb001', 'Buddy Black', 'larut101', 'Tony LaRussa', 'neshp001', 'Pat Neshek', 'augeb001', 'Bryan Augenstein', 'bellh001', 'Heath Bell', '', '(none)', 'staut001', 'Tim Stauffer', 'carpc002', 'Chris Carpenter', 'venaw001', 'Will Venable', '9', 'bartj001', 'Jason Bartlett', '6', 'hudso001', 'Orlando Hudson', '4', 'hawpb001', 'Brad Hawpe', '3', 'ludwr001', 'Ryan Ludwick', '7', 'headc001', 'Chase Headley', '5', 'maybc001', 'Cameron Maybin', '8', 'hundn001', 'Nick Hundley', '2', 'staut001', 'Tim Stauffer', '1', 'therr001', 'Ryan Theriot', '6', 'rasmc001', 'Colby Rasmus', '8', 'pujoa001', 'Albert Pujols', '3', 'hollm001', 'Matt Holliday', '7', 'berkl001', 'Lance Berkman', '9', 'freed001', 'David Freese', '5', 'moliy001', 'Yadier Molina', '2', 'schus001', 'Skip Schumaker', '4', 'carpc002', 'Chris Carpenter', '1', '', 'Y\n'], ['20110331', '0', 'Thu', 'ATL', 'NL', '1', 'WAS', 'NL', '1', '2', '0', '54', 'D', '', '', '', 'WAS11', '39055', '152', '110000000', '000000000', '31', '5', '1', '0', '1', '2', '0', '0', '0', '1', '0', '5', '0', '0', '1', '0', '3', '5', '0', '0', '0', '0', '27', '13', '0', '0', '0', '0', '31', '5', '1', '0', '0', '0', '0', '0', '0', '2', '0', '9', '0', '1', '0', '0', '6', '5', '2', '2', '0', '0', '27', '10', '0', '0', '1', '0', 'welkt901', 'Tim Welke', 'reynj901', 'Jim Reynolds', 'dimum901', 'Mike DiMuro', 'fleta901', 'Andy Fletcher', '', '(none)', '', '(none)', 'gonzf801', 'Fredi Gonzalez', 'riggj801', 'Jim Riggleman', 'lowed001', 'Derek Lowe', 'hernl003', 'Livan Hernandez', 'kimbc001', 'Craig Kimbrel', 'mccab002', 'Brian McCann', 'lowed001', 'Derek Lowe', 'hernl003', 'Livan Hernandez', 'pradm001', 'Martin Prado', '7', 'mclon001', 'Nate McLouth', '8', 'jonec004', 'Chipper Jones', '5', 'mccab002', 'Brian McCann', '2', 'uggld001', 'Dan Uggla', '4', 'heywj001', 'Jason Heyward', '9', 'gonza002', 'Alex Gonzalez', '6', 'freef001', 'Freddie Freeman', '3', 'lowed001', 'Derek Lowe', '1', 'desmi001', 'Ian Desmond', '6', 'wertj001', 'Jayson Werth', '9', 'zimmr001', 'Ryan Zimmerman', '5', 'laroa001', 'Adam LaRoche', '3', 'morsm001', 'Mike Morse', '7', 'ankir001', 'Rick Ankiel', '8', 'espid001', 'Danny Espinosa', '4', 'rodri001', 'Ivan Rodriguez', '2', 'hernl003', 'Livan Hernandez', '1', '', 'Y\n'], ['20110331', '0', 'Thu', 'ANA', 'AL', '1', 'KCA', 'AL', '1', '4', '2', '54', 'D', '', '', '', 'KAN06', '40055', '195', '000202000', '000000110', '38', '12', '4', '0', '2', '4', '1', '0', '1', '1', '0', '9', '1', '0', '0', '0', '10', '6', '2', '2', '0', '0', '27', '7', '0', '1', '0', '0', '33', '7', '0', '0', '2', '2', '0', '0', '0', '6', '0', '10', '1', '1', '0', '0', '10', '4', '3', '3', '0', '0', '27', '12', '3', '0', '0', '0', 'demud901', 'Dana DeMuth', 'danlk901', 'Kerwin Danley', 'nauep901', 'Paul Nauert', 'eddid901', 'Doug Eddings', '', '(none)', '', '(none)', 'sciom001', 'Mike Scioscia', 'yoste001', 'Ned Yost', 'weavj003', 'Jered Weaver', 'hochl001', 'Luke Hochevar', 'rodnf001', 'Fernando Rodney', 'huntt001', 'Torii Hunter', 'weavj003', 'Jered Weaver', 'hochl001', 'Luke Hochevar', 'iztum001', 'Maicer Izturis', '5', 'kendh001', 'Howie Kendrick', '4', 'abreb001', 'Bobby Abreu', '10', 'huntt001', 'Torii Hunter', '9', 'wellv001', 'Vernon Wells', '7', 'aybae001', 'Erick Aybar', '6', 'trumm001', 'Mark Trumbo', '3', 'mathj001', 'Jeff Mathis', '2', 'bourp001', 'Peter Bourjos', '8', 'avilm001', 'Mike Aviles', '5', 'cabrm002', 'Melky Cabrera', '8', 'gorda001', 'Alex Gordon', '7', 'butlb003', 'Billy Butler', '10', 'kaaik001', "Kila Ka'aihue", '3', 'franj004', 'Jeff Francoeur', '9', 'escoa003', 'Alcides Escobar', '6', 'tream001', 'Matt Treanor', '2', 'getzc001', 'Chris Getz', '4', '', 'Y\n'], ['20110331', '0', 'Thu', 'DET', 'AL', '1', 'NYA', 'AL', '1', '3', '6', '51', 'D', '', '', '', 'NYC21', '48226', '182', '010110000', '00300021x', '31', '6', '1', '0', '0', '3', '1', '2', '0', '2', '0', '10', '0', '0', '0', '0', '6', '4', '5', '5', '3', '0', '24', '9', '1', '0', '0', '0', '26', '5', '1', '0', '2', '6', '2', '1', '0', '5', '0', '8', '1', '0', '0', '0', '4', '4', '2', '2', '0', '0', '27', '4', '1', '0', '0', '0', 'scotd901', 'Dale Scott', 'mealj901', 'Jerry Meals', 'buckc901', 'CB Bucknor', 'iassd901', 'Dan Iassogna', '', '(none)', '', '(none)', 'leylj801', 'Jim Leyland', 'giraj001', 'Joe Girardi', 'chamj002', 'Joba Chamberlain', 'cokep001', 'Phil Coke', 'rivem002', 'Mariano Rivera', 'granc001', 'Curtis Granderson', 'verlj001', 'Justin Verlander', 'sabac001', 'CC Sabathia', 'jacka001', 'Austin Jackson', '8', 'rhymw001', 'Will Rhymes', '4', 'ordom001', 'Magglio Ordonez', '9', 'cabrm001', 'Miguel Cabrera', '3', 'martv001', 'Victor Martinez', '10', 'rabur001', 'Ryan Raburn', '7', 'peraj001', 'Jhonny Peralta', '6', 'ingeb001', 'Brandon Inge', '5', 'avila001', 'Alex Avila', '2', 'gardb001', 'Brett Gardner', '7', 'jeted001', 'Derek Jeter', '6', 'teixm001', 'Mark Teixeira', '3', 'rodra001', 'Alex Rodriguez', '5', 'canor001', 'Robinson Cano', '4', 'swisn001', 'Nick Swisher', '9', 'posaj001', 'Jorge Posada', '10', 'granc001', 'Curtis Granderson', '8', 'martr004', 'Russell Martin', '2', '', 'Y\n'])
        result_2012_10_3 = R._Researcher__get_list_of_games(date(2012, 10, 3))
        for index, game in enumerate(result_2012_10_3):
            self.assertEqual(listOfGames_2012_10_3[index], game)
        self.assertEqual(R._Researcher__get_list_of_games(date(2011, 3, 31)), 
                         listOfGames_2011_3_31)        

    @unittest.skip("Buffer thoroughly tested")
    def test_list_of_games_buffer(self):
        # Note: We only check the length of listOfGame, because checking 
        # exact output would be unseemly and frankly, unecessary
        d1 = date(2012, 5, 2)
        d2 = date(2011, 8, 4)
        d3 = date(2011, 6, 15)
        d4 = date(2011, 7, 11) # no games played
        d5 = date(2011, 7, 14)
        Edwin = p1
        Troy = Player("Troy", "Tulowitzki", 2010)
        Alfonso = Player("Alfonso", "Soriano", 2011)
        Albert = Player("Albert", "Pujols", 2012)
        Jose = p2

        ## CHECK 1: Not on buffer and last byte checked is of no use
            ## CHECK 1.1: If date slot is None, startSeekPos is 0 and buffer
            ## is updated with new date, listOfGames and lastByteChecked
        R.batterSetBuffer = [None, set([])]
        R.logUsedBuffer = False
        R.listOfGamesBuffer = (None, (), 0)
        R.find_home_team(d1, Edwin)
            # we didn't use the buffer
        self.assertFalse(R.logUsedBuffer)
            # buffer updated correctly
        self.assertEqual(R.logSeekPosUsed, 0)
        self.assertEqual(R.listOfGamesBuffer[0], d1)
        self.assertEqual(len(R.listOfGamesBuffer[1]), 15)
        self.assertEqual(R.listOfGamesBuffer[2], 397336)
            ## Check 1.2: If date slot is not none but it's a different year, 
            ## startSeekPos is 0 and buffer is updated with new date, 
            ## listOfGames and lastByteChecked
        R.batterSetBuffer = [None, set([])]
        R.logUsedBuffer = False
        R.find_home_team(d2, Troy)
            # we didn't use the buffer
        self.assertFalse(R.logUsedBuffer)
            # buffer updated correctly
        self.assertEqual(R.logSeekPosUsed, 0)
        self.assertEqual(R.listOfGamesBuffer[0], d2)
        self.assertEqual(len(R.listOfGamesBuffer[1]), 10)
        self.assertEqual(R.listOfGamesBuffer[2], 1801592)
            ## Check 1.2: If date slot is not none, its the same year, but
            ## the date is before the date on file,  then startSeekPos is 0
            ## and buffer is updated with new date, listOfGames, and lastByteChecked
        R.batterSetBuffer = [None, set([])]
        R.logUsedBuffer = False
        R.find_home_team(d3, Troy)
            # we didn't use the buffer
        self.assertFalse(R.logUsedBuffer)
            # buffer updated correctly
        self.assertEqual(R.logSeekPosUsed, 0)
        self.assertEqual(R.listOfGamesBuffer[0], d3)
        self.assertEqual(len(R.listOfGamesBuffer[1]), 16)
        self.assertEqual(R.listOfGamesBuffer[2], 1107385)

        ## CHECK 2: It's not on the buffer and last byte checked is of use
             ## Check 2.1: If there are no games today, (and current date is
             ## greater then last date checked etc) then startseekPos is 
             ## lastByteChecked, date is updated, it returns a () 
             ## and the last byte checked remains unchanged
        R.batterSetBuffer = [None, set([])]
        R.logUsedBuffer = False
        R.did_start_and_bat(d4, Alfonso) 
            # we didn't use the buffer
        self.assertFalse(R.logUsedBuffer)
            # buffer updated correctly
        self.assertEqual(R.logSeekPosUsed, 1107385)
        self.assertEqual(R.listOfGamesBuffer[0], d4)
        self.assertEqual(len(R.listOfGamesBuffer[1]), 0)
        self.assertEqual(R.listOfGamesBuffer[2], 1107385)
             ## Check 2.2: If there are games today, (and current date is greater
             ## than last date checked etc), then startSeekPos is lastByteCHecked,
             ## date is updated, it returns the correct listOfGames, and
             ## updates the last byte checked
        R.batterSetBuffer = [None, set([])]
        R.logUsedBuffer = False
        R.did_start_and_bat(d5, Troy)
            # we didn't use the buffer
        self.assertFalse(R.logUsedBuffer)
            # buffer updated correctly
        self.assertEqual(R.logSeekPosUsed, 1107385)
        self.assertEqual(R.listOfGamesBuffer[0], d5)
        self.assertEqual(len(R.listOfGamesBuffer[1]), 7)
        self.assertEqual(R.listOfGamesBuffer[2], 1487561)

        ## CHECK 3: If it's on the buffer, we get it from the buffer
        R.batterSetBuffer = [None, set([])]
        R.logUsedBuffer = False
        R.did_start_and_bat(d5, Alfonso)
          # we got it from the buffer
        self.assertTrue(R.logUsedBuffer)
          # buffer didn't change
        self.assertEqual(R.logSeekPosUsed, 1107385)
        self.assertEqual(R.listOfGamesBuffer[0], d5)
        self.assertEqual(len(R.listOfGamesBuffer[1]), 7)
        self.assertEqual(R.listOfGamesBuffer[2], 1487561)

        ## CHeck 4: If R looks up a hit on date d1, it can successfully 
        ## look up a hit for the FIRST listed game on the gamelog for date
        ## d1 + 1 day
        self.assertTrue(R.did_get_hit(date(2012, 6, 16), Jose))
        self.assertTrue(R.did_get_hit(date(2012, 6, 17), Albert))

    #@unittest.skip("Not Focus")
    def test_did_start_and_bat(self):
        self.assertFalse(R.did_start_and_bat(date(2011, 7, 2), p1))
        self.assertTrue(R.did_start_and_bat(date(2011, 9, 14), p2))
        self.assertFalse(R.did_start_and_bat(date(2012, 4, 15), p1))
        self.assertTrue(R.did_start_and_bat(date(2012, 4, 15), p2))
        self.assertTrue(R.did_start_and_bat(date(2009, 6, 17), p1))
        self.assertTrue(R.did_start_and_bat(date(2012, 4, 9), p2))
 
        # Adrian played in a game on 4/16 that was suspended and finished
        # on 4/17. He started on 4/16 and pinch ran on 4/17. Thus 
        # he should show up as NOT HAVING started on the 17th, and started on the 16th
        Adrian = Player("Adrian", "Beltre", 2010)
        self.assertFalse(R.did_start_and_bat(date(2010, 4, 17), Adrian))
        self.assertTrue(R.did_start_and_bat(date(2010, 4, 16), Adrian))

        # Craig started on the 07/30 but only pinch hit on 7/31. Thus he should
        # show up as NOT having started on the 31st, and starting on the 30th
        Craig = Player("Craig", "Biggio", 2004)
        self.assertFalse(R.did_start_and_bat(date(2004, 7, 31), Craig))
        self.assertTrue(R.did_start_and_bat(date(2004, 7, 3), Craig))

        ## A nationa lleague pitcher who started in a game at an American league
        ## park, and henece is in the gamelog, but did not bat
        self.assertFalse(R.did_start_and_bat(date(2012, 6, 11), p1)) # Edwin Jackson

    #@unittest.skip("Not Focus")
    def test_get_sus_Games_dict(self):
        participants_2001_6_15_s = (
          "welkt901","cedeg901","iassd901","hudsm901","muset101","loped001",
          "byrdp001","petek001","hernr001","beltc001","steib002","wrigj001",
          "chave002","sancr001","beltc001","sweem002","dye-j001","randj002",
          "alicl001","ortih001","steib002","sanca003","lorem001","jenkg001",
          "burnj001","sexsr001","hernj001","bellr002","blanh001","wrigj001")
        participants_2001_7_18_s = (
          "bellw901","mcclt901","barkl901","emmep901","brenb001","bochb002",
          "johnr005","willw001","gracm001","schic002","willw001","delld001",
          "bellj001","gonzl001","gracm001","willm003","finls001","milld002",
          "womat001","schic002","jackd003","kotsm001","klesr001","nevip001",
          "gwynt001","darrm001","gonzw001","jimed001","willw001"
          ) 
        participants_2011_4_8_s = (
          "hicke901","rapue901","onorb901","marqa901","mattd001","blacb001",
          "hawkb001","friee001","broxj001","gwynt002","lillt001","richc002",
          "furcr001","blakc001","ethia001","kempm001","uribj002","lonej001",
          "thamm001","barar001","lillt001","venaw001","bartj001","hudso001",
          "cantj001","ludwr001","headc001","maybc001","hundn001","richc002"
          )
        sGD2001 = {date(2001, 6, 15): (False, participants_2001_6_15_s),
                   date(2001, 7, 18): (False, participants_2001_7_18_s)}
        sGD2011 = {date(2011, 4, 8): (True, participants_2011_4_8_s)}
        self.assertDictEqual(R.get_sus_games_dict(2001), sGD2001)
        self.assertDictEqual(R.get_sus_games_dict(2011), sGD2011)

    #@unittest.skip("Not Focus")
    def test_num_at_bats(self):
        self.assertEqual(R.num_at_bats(2010, p1), 38) # traded from NL to AL
        self.assertEqual(R.num_at_bats(2006, p2), 647)
        self.assertEqual(R.num_at_bats(2005, p3), 637)
        self.assertEqual(R.num_at_bats(2001, p4), 484)
        self.assertEqual(R.num_at_bats(2008, p5), 552) # traded from BOS to LAD

    #@unittest.skip("Not Focus")
    def test_num_plate_appearances(self):
        self.assertEqual(R.num_plate_appearances(2010, p1), 43) # traded from NL to AL
        self.assertEqual(R.num_plate_appearances(2006, p2), 703)
        self.assertEqual(R.num_plate_appearances(2005, p3), 682)
        self.assertEqual(R.num_plate_appearances(2001, p4), 557)
        self.assertEqual(R.num_plate_appearances(2008, p5), 654) # traded from BOS to LAD

    #@unittest.skip("Not Focus")
    def test_name_from_lahman_id(self):
        self.assertEqual(R.name_from_lahman_id("jacksed01"), ("Edwin", "Jackson"))
        self.assertEqual(R.name_from_lahman_id("reyesjo01"), ("Jose",  "Reyes"))
        self.assertEqual(R.name_from_lahman_id("soriaal01"), ("Alfonso", "Soriano"))
        self.assertEqual(R.name_from_lahman_id("posadjo01"), ("Jorge", "Posada"))
        self.assertEqual(R.name_from_lahman_id("ramirma02"), ("Manny", "Ramirez"))
        self.assertEqual(R.name_from_lahman_id("loducpa01"), ("Paul", "Lo Duca"))

    #@unittest.skip("Not Focus")
    def test_get_opening_day(self):
        self.assertEqual(R.get_opening_day(2010), date(2010,4,4))
        self.assertEqual(R.get_opening_day(1992), date(1992, 4,6))

    #@unittest.skip("Not Focus")
    def test_get_closing_day(self):
        self.assertEqual(R.get_closing_day(2010), date(2010,10,3))
        self.assertEqual(R.get_closing_day(1992), date(1992, 10,4))

    #@unittest.skip("Not Focus")
    def test_check_date(self):
        self.assertRaises(BadDateException, R.check_date, date(2010, 3, 1), 
            2010)
        self.assertRaises(BadDateException, R.check_date, date(1950, 3, 7), 
          1950)

    #@unittest.skip("Not Focus")
    def test_is_game_suspended(self):
        ## The first four lines of testResearcher_is_game_suspended.txt 
        ## are the gamelog lines for the below four games
        os.chdir(Filepath.get_root() + "/tests/")
        testFile = open("testResearcher_is_game_suspended.txt")

        line = testFile.readline() # april 16th, 2010, TBR at BOS (sus)
        self.assertTrue(R._Researcher__is_game_suspended(line))

        line = testFile.readline() # may 1st, 2007, PIT at CHC (sus)
        self.assertTrue(R._Researcher__is_game_suspended(line))

        line = testFile.readline() # sep 3, 2007, KCR at TEX (sus)
        self.assertFalse(R._Researcher__is_game_suspended(line))

        line = testFile.readline() # August 30th, 2002 NYY at TOR (sus)
        self.assertFalse(R._Researcher__is_game_suspended(line))

        testFile.close()

    #@unittest.skip("Not Focus")
    def test_is_suspended_game_valid(self):
        ## The first four lines of testResearcher_is_suspended_game_valid.txt
        ## are the gamelog lines for the below four games
        os.chdir(Filepath.get_root() + "/tests")
        testFile = open("testResearcher_is_suspended_game_valid.txt")

        ## Cases where >= 5 innings played (Valid)
        line = testFile.readline() # May 1st 2007, CHN #@ PIT
        self.assertTrue(R._Researcher__is_suspended_game_valid(line))

        line = testFile.readline() # April 12th 2000, LAN #@ SFN
        self.assertTrue(R._Researcher__is_suspended_game_valid(line))

        ## Cases with <= 4 innings played (Invalid)
        line = testFile.readline() # June 15th 2001, KCA @ MIL
        self.assertFalse(R._Researcher__is_suspended_game_valid(line))

        line = testFile.readline() # July 18th 2001, ARI #@ SDN
        self.assertFalse(R._Researcher__is_suspended_game_valid(line))

        ### The rest of the games are made up in order to test corner cases

        ## Valid: suspended in the fifth, vistotrs trail, >= 3 outs played
        line = testFile.readline()
        self.assertTrue(R._Researcher__is_suspended_game_valid(line))
        ## Valid: suspended in the 5th, tied game, >= 3 outs done
        line = testFile.readline()
        self.assertTrue(R._Researcher__is_suspended_game_valid(line))

        ## Invalid: sus in 5th, visitors trail, <= 2 outs played
        line = testFile.readline()
        self.assertFalse(R._Researcher__is_suspended_game_valid(line))
        ## Invalid: sus in 5th, visitors lead, <= 5 outs played
        line = testFile.readline()
        self.assertFalse(R._Researcher__is_suspended_game_valid(line))
        ## Invalid: sus in 5th, game tied, <= 2 outs played
        line = testFile.readline()
        self.assertFalse(R._Researcher__is_suspended_game_valid(line))

        ## Should throw an exception if given a not suspended game
        line = testFile.readline()
        self.assertRaises(NotSuspendedGameException, 
            R._Researcher__is_suspended_game_valid, line)

        testFile.close()

    def test_opposing_pitcher_era(self):
        Jose = p2
        Pat = Player('Pat', 'Meares', 1997)
        Doug = Player('Doug', 'Mirabelli', 2000)
        Jacoby = Player('Jacoby', 'Ellsbury', 2012) 
        Ryan = Player('Ryan', 'Langerhans', 2011)
        David = Player("David", "Murphy", 2011)
        Jack = Player("Jack", "Wilson", 2005, debut='4/3/2001')

        # Testing different points in the season
        self.assertEqual(R.opposing_pitcher_era(Ryan, date(2011,4,1)), float('inf')) # Opening Day
        self.assertEqual(R.opposing_pitcher_era(Pat, date(1997,6,16)), 5.53) # Middle of the season
            # added bonus: pitcher has an asterisk next to his statline in the boxscore
        self.assertEqual(R.opposing_pitcher_era(Jacoby, date(2011,9,28)), 4.85) # Closing Day

        # Testing home and away pitchers
        self.assertEqual(R.opposing_pitcher_era(Jose, date(2009,5,10)), 4.50) # visiting pitcher
        self.assertEqual(R.opposing_pitcher_era(Doug, date(2000,9,27)), 1.69) # home pitcher

        # Testing multiple or single appeareacnes in the boxscore
            # Pitcher: CC Sabathia. ONLY PITCHED (All AL Games)
        self.assertEqual(R.opposing_pitcher_era(David, date(2011, 4, 17)), 1.45)
            # Pitcher: Derek Lowe. PITCHED AND BATTED (NL Games)
        self.assertEqual(R.opposing_pitcher_era(Jack, date(2005, 8, 5)), 3.99)
        
        

    def test_create_player_hit_info_csv(self):        
        ## Test 1
        ## Create a player hit info csv and check all the vals
        Derek = Player("Derek", "Jeter", 2010)
        R.create_player_hit_info_csv(Derek, 2006)
        sGD2006 = R.get_sus_games_dict(2006)

        df = DataFrame.from_csv(Filepath.get_player_hit_info_csv_file(
                                Derek.get_lahman_id(), 2006))
        for date, hitVal, otherInfo, opPitcherEra in df.itertuples():
            datetimeDate = datetime.date(2006, date.month, date.day)
            if otherInfo == 'n/a':
                otherInfo = None
            if hitVal == 'True':
                hitVal = True
            if hitVal == 'False':
                hitVal = False
            self.assertEqual( (hitVal, otherInfo), 
                               R.get_hit_info(datetimeDate, Derek, sGD2006))
            self.assertEqual( opPitcherEra, 
                              R.opposing_pitcher_era(Derek, datetimeDate) )

        ## Test 2
        ## Create a player hit info csv and check all vals
        Endy = Player("Endy", "Chavez", 2001)
        R.create_player_hit_info_csv(Endy, 2001)
        sGD2001 = R.get_sus_games_dict(2001)
        df = DataFrame.from_csv(Filepath.get_player_hit_info_csv_file(
                                Endy.get_lahman_id(), 2001))
        for date, hitVal, otherInfo, opPitcherEera in df.itertuples():
            datetimeDate = datetime.date(2001, date.month, date.day)
            if otherInfo == 'n/a':
                otherInfo = None
            if hitVal == 'True':
                hitVal = True
            if hitVal == 'False':
                hitVal = False
            self.assertEqual( (hitVal, otherInfo), 
                               R.get_hit_info(datetimeDate, Endy, sGD2001))
            self.assertEqual( opPitcherEra, 
                              R.opposing_pitcher_era(Eddy, datetimeDate) )