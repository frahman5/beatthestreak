import unittest
import os

from datetime import date

from beatthestreak.filepath import Filepath
from beatthestreak.researcher import Researcher as R
from beatthestreak.tests import setup, teardown, p1, p2, p3, p4, p5
from beatthestreak.player import PlayerL, Player
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
participants_2013_6_7 = ['reynj901', 'hoyej901', 'hirsj901', 'davib902', 'melvb001', 'coopd001', 'parkj001', 'salec001', 'balfg001', 'donaj001', 'parkj001', 'salec001', 'crisc001', 'lowrj001', 'cespy001', 'donaj001', 'frein001', 'younc004', 'reddj001', 'norrd001', 'rosaa001', 'deaza001', 'ramia003', 'riosa002', 'dunna001', 'vicid001', 'gillc001', 'beckg001', 'dankj002', 'flowt001', 'holbs901', 'fleta901', 'drakr901', 'westj901', 'frant001', 'leylj801', 'verlj001', 'jimeu001', 'martv001', 'jimeu001', 'verlj001', 'bourm001', 'kipnj001', 'swisn001', 'branm003', 'santc002', 'reynm001', 'giamj001', 'avilm001', 'stubd001', 'dirka001', 'huntt001', 'cabrm001', 'fielp001', 'martv001', 'peraj001', 'penab002', 'santr002', 'garca003', 'gormb901', 'gonzm901', 'randt901', 'vanol901', 'portb001', 'yoste001', 'herrk001', 'wrigw001', 'hollg001', 'butlb003', 'lylej001', 'shiej002', 'barnb002', 'crowt001', 'castj006', 'martj006', 'penac001', 'cartc002', 'ceder002', 'domim001', 'gonzm002', 'gorda001', 'hosme001', 'peres002', 'butlb003', 'cainl001', 'lougd001', 'tejam001', 'getzc001', 'escoa003', 'wegnm901', 'diazl901', 'muchm901', 'wintm901', 'giraj001', 'wedge001', 'bondj001', 'kuroh001', 'wilht001', 'ryanb002', 'kuroh001', 'bondj001', 'gardb001', 'canor001', 'teixm001', 'hafnt001', 'youkk001', 'wellv001', 'suzui001', 'brigr001', 'stewc001', 'chave002', 'bay-j001','seagk001', 'morak001', 'ibanr001', 'morsm001', 'frann001', 'shopk001', 'ryanb002', 'barrl901', 'barkl901', 'cedeg901', 'carav901', 'showb801', 'maddj801', 'archc001', 'hammj002', 'rodnf001', 'jennd002', 'hammj002', 'archc001', 'mclon001', 'machm001', 'markn001', 'jonea003', 'davic003', 'wietm001', 'hardj003', 'dickc001', 'flahr001', 'joycm001', 'zobrb001', 'johnk003', 'longe001', 'lonej001', 'jennd002', 'scotl001', 'molij001', 'escoy001', 'mealj901', 'drecb901', 'darlg901', 'emmep901', 'washr001', 'gibbj001', 'wagnn001', 'tepen001', 'encae001', 'tepen001', 'rogee002', 'andre001', 'profj001', 'piera001', 'belta001', 'bakej001', 'murpd005', 'gentc001', 'mcguc001', 'martl004', 'cabrm002', 'bautj002', 'encae001', 'linda001', 'arenj001', 'rasmc001', 'iztum001', 'bonie001', 'kawam001', 'porta901', 'laynj901', 'gibsg901', 'wendh902', 'bochb002', 'gibsk001', 'ziegb001', 'affej001', 'bellh001', 'goldp001', 'cainm001', 'corbp001', 'torra001', 'scutm001', 'poseb001', 'pench001', 'sandp001', 'beltb001', 'crawb001', 'blang001', 'cainm001', 'parrg001', 'bloow001', 'goldp001', 'montm001', 'rossc001', 'pradm001', 'gregd001', 'polla001', 'corbp001', 'gibsg901', 'bakej902', 'demud901', 'nauep901', 'herna901', 'hurdc001', 'sveud001', 'lirif001', 'woodt004', 'grilj001', 'martr004', 'lirif001', 'woodt004', 'marts002', 'mercj002', 'mccua001', 'sancg001', 'martr004', 'alvap001', 'walkn001', 'snidt001', 'lirif001', 'barnd001', 'ransc001', 'rizza001', 'soria001', 'hairs001', 'castw002', 'casts001', 'sweer001', 'woodt004', 'guccc901', 'estam901', 'cuzzp901', 'hallt901', 'mathm001', 'baked002', 'waina001', 'leakm001', 'freed001', 'waina001', 'leakm001', 'carpm002', 'beltc001', 'hollm001', 'craia001', 'moliy001', 'freed001', 'jay-j001','kozmp001', 'waina001', 'choos001', 'cozaz001', 'vottj001', 'philb001', 'brucj001', 'frazt001', 'paulx001', 'mesod001', 'leakm001', 'hicke901', 'joycj901', 'blasc901', 'nelsj901', 'blacb001', 'weisw001', 'belim001', 'thatj001', 'arenn001', 'volqe001', 'delaj001', 'denoc001', 'cabre001', 'headc001', 'quenc001', 'gyorj001', 'blank002', 'maybc001', 'grany001', 'volqe001', 'fowld001', 'youne003', 'gonzc001', 'tulot001', 'heltt001', 'arenn001', 'lemad001', 'torry001', 'delaj001', 'scotd901', 'buckc901', 'reybd901', 'ticht901', 'gonzf801', 'mattd001', 'leagb001', 'varva001', 'mahop002', 'ryu-h001', 'simma001', 'heywj001', 'uptoj001', 'freef001', 'gatte001', 'johnc003', 'uggld001', 'uptob001', 'mahop002', 'puigy001', 'ellim001', 'gonza003', 'vanss001', 'hairj002', 'ethia001', 'hernr002', 'cruzl001', 'ryu-h001','tumpj901', 'carlm901', 'knigb901', 'iassd901', 'manuc101', 'roenr001', 'rodrf003', 'horsj001', 'ramia001','lee-c003', 'figaa001', 'younm003', 'maybj001', 'rollj001', 'howar001', 'browd004', 'yound003', 'krate001', 'galvf001', 'lee-c003', 'aokin001', 'seguj002', 'braur002', 'ramia001', 'lucrj001', 'gomec002', 'weekr001', 'betay001', 'figaa001']
participants_2009_7_9 = ['meric901', 'diazl901', 'coope901', 'reilm901', 'gonzf801', 'hinca001', 'calek001', 'schos001', 'carrb001', 'milla002', 'petiy001', 'coghc001', 'bonie001', 'uggld001', 'cantj001', 'rossc001', 'hermj001', 'bakej002', 'helmw001', 'milla002', 'lopef001', 'ojeda001', 'uptoj001', 'reynm001', 'parrg001', 'younc004', 'clart002', 'carll001', 'petiy001', 'drakr901', 'schrp901', 'nauep901', 'westj901', 'cox-b103', 'tracj101', 'rincj001', 'gonzm001', 'streh001', 'atkig001', 'hanst001', 'cooka002', 'mclon001', 'pradm001', 'andeg001', 'mccab002', 'escoy001', 'kotcc001', 'franj004', 'conrb001', 'hanst001', 'fowld001', 'barmc001', 'heltt001', 'hawpb001', 'tulot001', 'stewi001', 'iannc001', 'gonzc001', 'cooka002', 'wolfj901', 'onorb901', 'culbf901', 'johna901', 'actam801', 'coopc001', 'ariaa002', 'lannj001', 'bourm001', 'lannj001', 'ortir001', 'morgn001', 'johnn001', 'zimmr001', 'dunna001', 'willj004', 'guzmc001', 'bardj001', 'herna003', 'lannj001', 'bourm001', 'tejam001', 'berkl001', 'lee-c001', 'pench001', 'rodri001', 'blumg001', 'keppj001', 'ortir001', 'emmep901', 'darlg901', 'hohnb901', 'drecb901', 'larut101', 'machk101', 'pinej001', 'villc001', 'pujoa001', 'pinej001', 'parrm001', 'ryanb002', 'rasmc001', 'pujoa001', 'ludwr001', 'stavn001', 'moliy001', 'hoffj002', 'pinej001', 'bardb001', 'counc001', 'hardj003', 'braur002', 'fielp001', 'mcgec001', 'camem001', 'cataf001', 'rivem003', 'parrm001', 'fostm901', 'fairc901', 'hirsj901', 'bellw901', 'torrj101', 'manuj101', 'wolfr001', 'hernl003', 'ramim002', 'wolfr001', 'hernl003', 'furcr001', 'ethia001', 'ramim002', 'blakc001', 'lonej001', 'martr004', 'hudso001', 'kempm001', 'wolfr001', 'castl001', 'evann001', 'wrigd002', 'shefg001', 'tatif001', 'churr001', 'santo001', 'coraa001', 'hernl003', 'scotd901', 'mealj901', 'dimum901', 'kulpr901', 'baked002', 'manuc101', 'moyej001', 'owinm001', 'lidgb001', 'rollj001', 'owinm001', 'moyej001', 'tavew001', 'dickc001', 'vottj001', 'philb001', 'hernr002', 'gomej001', 'encae001', 'janip001', 'owinm001', 'rollj001', 'victs001', 'utlec001', 'howar001', 'wertj001', 'dobbg001', 'felip001', 'ruizc001', 'moyej001', 'cuzzp901', 'rungb901', 'hallt901', 'campa902', 'blacb001', 'bochb002', 'linct001', 'geerj001', 'molib001', 'geerj001', 'linct001', 'cabre001', 'gwynt002', 'gonza003', 'kouzk001', 'headc001', 'venaw001', 'alfoe002', 'rodrl002', 'geerj001', 'winnr001', 'schin001', 'sandp001', 'molib001', 'bowkj001', 'rente001', 'ishit001', 'uribj002', 'linct001', 'millb901', 'cousd901', 'ticht901', 'joycj901', 'hillt801', 'frant001', 'hochl001', 'mastj001', 'sorij001', 'dejed001', 'hochl001', 'pennb002', 'dejed001', 'bloow001', 'butlb003', 'guilj001', 'teahm001', 'jacom001', 'olivm001', 'calla001', 'freer001', 'drewj001', 'pedrd001', 'youkk001', 'ortid001', 'bay-j001', 'ellsj001', 'varij001', 'kotsm001', 'green001', 'tscht901', 'davib902', 'nelsj901', 'carlm901', 'wedge001', 'guilo001', 'sippt001', 'richc002', 'woodk002', 'shopk001', 'huffd001', 'richc002', 'cabra002', 'sizeg001', 'martv001', 'choos001', 'peraj001', 'garkr001', 'carrj001', 'franb001', 'shopk001', 'podss001', 'ramia003', 'dye-j001','thomj002', 'konep001', 'piera001', 'nix-j001', 'getzc001', 'beckg001', 'timmt901', 'wegnm901', 'kellj901', 'barrs901', 'giraj001', 'gardr001', 'albaj001', 'lirif001', 'rivem002', 'ransc001', 'aceva001', 'lirif001', 'jeted001', 'swisn001', 'teixm001', 'rodra001', 'posaj001', 'canor001', 'cabrm002', 'ransc001', 'gardb001', 'spand001', 'tolbm001', 'mauej001', 'mornj001', 'kubej002', 'cuddm001', 'buscb001', 'redmm001', 'puntn001', 'holbs901', 'iassd901', 'relic901', 'vanol901', 'washr001', 'wakad001', 'hernf002', 'wilsc004', 'aardd001', 'gutif001', 'huntt002', 'hernf002', 'kinsi001', 'younm003', 'hamij003', 'jonea002', 'blalh001', 'byrdm001', 'murpd005', 'saltj001', 'andre001', 'suzui001', 'branr001', 'lopej003', 'grifk002', 'gutif001', 'langr002', 'woodc001', 'johnr009', 'ceder002', 'welkt901', 'reynj901', 'hoyej901', 'welkb901', 'gastc101', 'maddj801', 'pricd001', 'hallr001', 'wheed001', 'penac001', 'hallr001', 'pricd001', 'bautj002', 'hilla001', 'linda001', 'millk005', 'wellv001', 'riosa002', 'overl001', 'barar001', 'mcdoj003', 'uptob001', 'crawc002', 'longe001', 'penac001', 'zobrb001', 'burrp001', 'grosg002', 'bartj001', 'hernm002']
participants_2007_5_2 = ['drakr901', 'rapue901', 'hicke901', 'westj901', 'manuc101', 'cox-b103', 'paroc001', 'garcf002', 'sorir001', 'harrw001', 'garcf002', 'jamec002', 'rollj001', 'rowaa001', 'utlec001', 'howar001', 'burrp001', 'helmw001', 'wertj001', 'barar001', 'garcf002', 'johnk003', 'rente001', 'jonec004', 'jonea002', 'thors001', 'franj004', 'saltj001', 'harrw001', 'jamec002', 'tscht901', 'joycj901', 'nelsj901', 'wolfj901', 'narrj001', 'garnp001', 'oswar001', 'lohsk001', 'wheed001', 'pench001', 'lohsk001', 'oswar001', 'freer001', 'hatts001', 'philb001', 'grifk002', 'gonza002', 'dunna001', 'hamij003', 'valej004', 'lohsk001', 'biggc001', 'pench001', 'berkl001', 'lee-c001', 'lorem001', 'scotl001', 'evera001', 'ausmb001', 'oswar001', 'reynj901', 'guccc901', 'cedeg901', 'barkl901', 'melvb001', 'littg801', 'hendm001', 'david002', 'saitt001', 'pierj002', 'david002', 'hendm001', 'younc004', 'jackc002', 'hudso001', 'byrne001', 'quenc001', 'drews001', 'snydc002', 'bardb001', 'david002', 'furcr001', 'pierj002', 'garcn001', 'kentj001', 'martr004', 'betew001', 'ethia001', 'clarb003', 'hendm001', 'scotd901', 'emmep901', 'iassd901', 'kulpr901', 'larut101', 'yoste001', 'villc001', 'reyea002', 'hartc001', 'reyea002', 'capuc001', 'tagus001', 'duncc002', 'pujoa001', 'roles001', 'spies001', 'benng001', 'milea001', 'ecksd001', 'reyea002', 'weekr001', 'hardj003', 'fielp001', 'hallb001', 'jenkg001', 'hartc001', 'milld002', 'graft001', 'capuc001', 'nauep901', 'gormb901', 'davig901', 'everm901', 'gonzf801', 'randw001', 'pereo002', 'sanca004', 'wagnb001', 'reyej001', 'sanca004', 'pereo002', 'ramih003', 'uggld001', 'cabrm001', 'willj004', 'boona001', 'rossc001', 'borcj001', 'tream001', 'sanca004', 'reyej001', 'chave002', 'beltc001', 'delgc001', 'wrigd002', 'grees001', 'castr002', 'gotar001', 'pereo002', 'hudsm901', 'barrt901', 'monte901', 'millb901', 'pinil001', 'tracj101', 'marqj001', 'sneli001', 'soria001', 'marqj001', 'sneli001', 'soria001', 'therr001','lee-d002', 'ramia001', 'floyc001', 'barrm003', 'jonej003', 'iztuc001', 'marqj001', 'duffc001', 'wilsj002', 'sancf001', 'bay-j001', 'laroa001', 'doumr001', 'bautj002', 'paulr001', 'sneli001', 'culbf901', 'darlg901', 'fostm901', 'schrp901', 'actam801', 'blacb001', 'brocd001', 'chicm001', 'kouzk001', 'chicm001', 'hensc002', 'lopef001', 'bellr002', 'zimmr001', 'churr001', 'keara001', 'schnb001', 'fickr001', 'castk001', 'chicm001', 'gilem001', 'cruzj004', 'gileb002', 'gonza003', 'greek002', 'bardj001', 'camem001', 'kouzk001', 'hensc002', 'hoyej901', 'reilm901', 'kellj901', 'coope901', 'hurdc001', 'bochb002', 'hennb001', 'franj003', 'bondb001', 'franj003', 'zitob001', 'tavew001', 'tulot001', 'hollm001', 'heltt001', 'atkig001', 'hawpb001', 'iannc001', 'carrj001', 'franj003', 'robed001', 'winnr001', 'aurir001', 'bondb001', 'durhr001', 'molib001', 'felip001', 'niekl001', 'zitob001', 'vanol901', 'gibsg901', 'hallt901', 'relic901', 'gereb001', 'frant001', 'beckj002', 'marsj001', 'timlm001', 'lugoj001', 'gaudc001', 'beckj002', 'stews002', 'ellim001', 'chave001', 'piazm001', 'johnd004', 'crosb002', 'putnd001', 'kendj001', 'langr002', 'lugoj001', 'youkk001', 'ortid001', 'ramim002', 'drewj001', 'lowem001', 'varij001', 'crisc001', 'coraa001', 'holbs901', 'wendh902', 'marsr901', 'davib902', 'gibbj001', 'wedge001', 'mastt001', 'marcs001', 'hafnt001', 'zambv001', 'westj001', 'riosa002', 'linda001', 'wellv001', 'thomf001', 'overl001', 'glaut001', 'hilla001', 'clayr001', 'fasas001', 'sizeg001', 'delld001', 'hafnt001', 'martv001', 'nixot001', 'garkr001', 'peraj001', 'blakc001', 'barfj003', 'muchm901', 'welkb901', 'bellw901', 'diazl901', 'perls101', 'leylj801', 'roben001', 'tracs001', 'jonet003', 'monrc001', 'tracs001', 'roben001', 'robeb003', 'paytj001', 'tejam001', 'hernr002', 'moram002', 'millk005', 'markn001', 'gomec001', 'pattc001', 'granc001', 'polap001', 'shefg001', 'ordom001', 'rodri001', 'cases001', 'monrc001', 'ingeb001', 'infao001', 'mcclt901', 'poncl901', 'mealj901', 'drecb901', 'sciom001', 'bellb001', 'delaj001', 'sante001', 'sorij001', 'germe001', 'sante001', 'delaj001', 'mattg002', 'willr004', 'cabro001', 'guerv001', 'quinr002', 'hills002', 'aybae001', 'napom001', 'figgc001', 'dejed001', 'germe001', 'teahm001', 'sandr002', 'gloar001', 'gorda001', 'butlb003', 'penat002', 'laruj001', 'reedr901', 'meric901', 'marqa901', 'timmt901', 'guilo001', 'hargm001', 'batim001', 'dankj001', 'putzj001', 'betay001', 'dankj001', 'batim001', 'erstd001', 'iguct001', 'piera001', 'konep001', 'dye-j001', 'mackr001', 'credj001', 'sweer001', 'uribj002', 'suzui001', 'belta001', 'vidrj001', 'ibanr001', 'sexsr001', 'guilj001', 'johjk001', 'betay001', 'lopej003', 'younl901', 'herna901', 'laynj901', 'carlm901', 'gardr001', 'maddj801', 'reyea001', 'guerm001', 'navad001', 'bonsb001', 'seo-j001','castl001', 'puntn001', 'mauej001', 'mornj001', 'huntt001', 'kubej002', 'cirij001', 'tynej001', 'bartj001', 'baldr001', 'dukee001', 'crawc002', 'wiggt001', 'yound003', 'uptob001', 'penac001', 'harrb001', 'paulj001']

class TestResearcher(unittest.TestCase):
    
    def setUp(self):
        setup()
        self.maxDiff = None
        
    def tearDown(self):
        teardown()
    
    # @unittest.skip("Too long")
    def test_did_get_hit(self):
        # Edwin Jackon test
        self.assertFalse(R.did_get_hit(date(2012, 5, 2), p1))

        # Jose Reyes Tests
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

        ## Larry Jones, from PlayerL, test. Tests to see if it works even if
        ## the player has a nickname (Goes by Chipper instead of Larry)
        pL = PlayerL('jonesch06', 2003)
        pL = Player(0, playerL=pL)
        self.assertTrue(R.did_get_hit(date(2003, 4, 19), pL))
        self.assertFalse(R.did_get_hit(date(2003, 8, 28), pL))

        # Test Miguel Cabrera, Asdrubal Cabrera, Delmon Young, Michael Young.
        # Checks for proper answer when the functional line of the boxscore
        # has two players with the same last name
        MC1 = Player(0, "Miguel", "Cabrera", 2012)
        MC2 = Player(1, "Asdrubal", "Cabrera", 2012)
        dateMC = date(2012, 9, 5)
        self.assertTrue(R.did_get_hit(dateMC, MC1))
        self.assertFalse(R.did_get_hit(dateMC, MC2))

        MY1 = Player(2, "Michael", "Young", 2012)
        MY2 = Player(3, "Delmon", "Young", 2012)
        dateMY = date(2012, 6, 26)
        self.assertTrue(R.did_get_hit(dateMY, MY1))
        self.assertFalse(R.did_get_hit(dateMY, MY2))

        ## Double Header tests (its a hit iff player got a hit in first game)
        self.assertFalse(R.did_get_hit(date(1996, 9, 25), p4)) # T1, H2
        self.assertFalse(R.did_get_hit(date(2008, 9, 7), p2)) # T1, T2
        self.assertTrue(R.did_get_hit(date(2007, 7, 28), p2)) # H1, T2
        self.assertTrue(R.did_get_hit(date(2006, 6, 3), p2)) # H1, H2

        # Lance Berkman tests
        Lance = Player(0, "Lance", "Berkman", 2008)
        self.assertTrue(R.did_get_hit(date(2009, 7, 9), Lance))

    def test_get_participants(self):
    	self.assertEqual(R.get_participants(date(2011,9,4)), 
            participants_2011_9_4)
        self.assertEqual(R.get_participants(date(2012,3,28)), 
            participants_2012_3_28)
        self.assertEqual(R.get_participants(date(2013,6,7)), 
            participants_2013_6_7)

        # Given a suspended game s1 that was started on date d1 and completed on
        # date d2, get_participants(d2) should NOT return players from d1
        self.assertEqual(R.get_participants(date(2009, 7, 9)), 
            participants_2009_7_9) # May 5th HOU @ WAS susp game completed on July 9th
        self.assertEqual(R.get_participants(date(2007, 5, 2)), 
            participants_2007_5_2) # May 1st CHN @ PIT suspended game completed on May 2

    def test_find_home_team(self):
    	self.assertEqual(R.find_home_team(date(2011, 8, 3), p1), "MIL")
        self.assertEqual(R.find_home_team(date(2012, 5, 2), p1), "WAS")
        self.assertEqual(R.find_home_team(date(2012, 6, 15), p2), "TBA")
        self.assertEqual(R.find_home_team(date(2013, 9, 20), p2), "BOS")

    def test_did_start(self):
        self.assertFalse(R.did_start(date(2011, 7, 2), p1))
        self.assertTrue(R.did_start(date(2011, 9, 14), p2))
        self.assertFalse(R.did_start(date(2012, 4, 15), p1))
        self.assertTrue(R.did_start(date(2012, 4, 15), p2))
        self.assertTrue(R.did_start(date(2013, 5, 17), p1))
        self.assertTrue(R.did_start(date(2013, 8, 11), p2))
 
        # Adrian played in a game on 4/16 that was suspended and finished
        # on 4/17. He started on 4/16 and pinch ran on 4/17. Thus 
        # he should show up as NOT HAVING started on the 17th, and started on the 16th
        Adrian = Player(1, "Adrian", "Beltre", 2010)
        self.assertFalse(R.did_start(date(2010, 4, 17), Adrian))
        self.assertTrue(R.did_start(date(2010, 4, 16), Adrian))

        # Craig started on the 07/30 but only pinch hit on 7/31. Thus he should
        # show up as NOT having started on the 31st, and starting on the 30th
        Craig = Player(2, "Craig", "Biggio", 2004)
        self.assertFalse(R.did_start(date(2004, 7, 31), Craig))
        self.assertTrue(R.did_start(date(2004, 7, 3), Craig))

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

    def test__search_file(self):
        os.chdir(Filepath.get_root() + "/tests/")
        testFile = open("testResearcher.txt")
        self.assertIsNotNone(R._Researcher__search_file(testFile, "Omega"))
        self.assertRaises(FileContentException, R._Researcher__search_file, 
           testFile, "fifty")
        testFile.close()

    def test_num_at_bats(self):
        self.assertEqual(R.num_at_bats(2010, p1), 38) # traded from NL to AL
        self.assertEqual(R.num_at_bats(2006, p2), 647)
        self.assertEqual(R.num_at_bats(2005, p3), 637)
        self.assertEqual(R.num_at_bats(2001, p4), 484)
        self.assertEqual(R.num_at_bats(2008, p5), 552) # traded from BOS to LAD

    def test_num_plate_appearances(self):
        self.assertEqual(R.num_plate_appearances(2010, p1), 43) # traded from NL to AL
        self.assertEqual(R.num_plate_appearances(2006, p2), 703)
        self.assertEqual(R.num_plate_appearances(2005, p3), 682)
        self.assertEqual(R.num_plate_appearances(2001, p4), 557)
        self.assertEqual(R.num_plate_appearances(2008, p5), 654) # traded from BOS to LAD

    def test_name_from_lahman_id(self):
        self.assertEqual(R.name_from_lahman_id("jacksed01"), ("Edwin", "Jackson"))
        self.assertEqual(R.name_from_lahman_id("reyesjo01"), ("Jose",  "Reyes"))
        self.assertEqual(R.name_from_lahman_id("soriaal01"), ("Alfonso", "Soriano"))
        self.assertEqual(R.name_from_lahman_id("posadjo01"), ("Jorge", "Posada"))
        self.assertEqual(R.name_from_lahman_id("ramirma02"), ("Manny", "Ramirez"))
        self.assertEqual(R.name_from_lahman_id("loducpa01"), ("Paul", "Lo Duca"))

    def test_get_opening_day(self):
        self.assertEqual(R.get_opening_day(2010), date(2010,4,4))
        self.assertEqual(R.get_opening_day(1992), date(1992, 4,6))

    def test_get_closing_day(self):
        self.assertEqual(R.get_closing_day(2010), date(2010,10,3))
        self.assertEqual(R.get_closing_day(1992), date(1992, 10,4))

    def test_check_date(self):
        self.assertRaises(BadDateException, R.check_date, date(2010, 3, 1), 
            2010)

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

    def test_is_suspended_game_valid(self):
        ## The first four lines of testResearcher_is_suspended_game_valid.txt
        ## are the gamelog lines for the below four games
        os.chdir(Filepath.get_root() + "/tests")
        testFile = open("testResearcher_is_suspended_game_valid.txt")

        ## Cases where >= 5 innings played (Valid)
        line = testFile.readline() # May 1st 2007, CHN @ PIT
        self.assertTrue(R._Researcher__is_suspended_game_valid(line))

        line = testFile.readline() # April 12th 2000, LAN @ SFN
        self.assertTrue(R._Researcher__is_suspended_game_valid(line))

        ## Cases with <= 4 innings played (Invalid)
        line = testFile.readline() # June 15th 2001, KCA @ MIL
        self.assertFalse(R._Researcher__is_suspended_game_valid(line))

        line = testFile.readline() # July 18th 2001, ARI @ SDN
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