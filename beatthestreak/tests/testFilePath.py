import unittest

from datetime import date

from beatthestreak.filepath import Filepath
from beatthestreak.tests import setup, teardown
from beatthestreak.exception import BadFilepathException
from beatthestreak.config import rootDir

class TestFilepath(unittest.TestCase):
    """
    As these tests use filepaths native to the development
    machine, they only work on the development machine
    """

    def setUp(self):
        self.rootDir = rootDir
        setup()
        
    def tearDown(self):
        teardown()

    def test_get_root(self):
        self.assertEqual(Filepath.get_root(),self.rootDir)

    def test_get_retrosheet_folder(self):
        # test top level folders
        self.assertEqual(Filepath.get_retrosheet_folder(folder='base'), 
            self.rootDir + '/datasets/retrosheet')
        self.assertEqual(Filepath.get_retrosheet_folder(folder='zipped'), 
            self.rootDir + '/datasets/retrosheet/zipped')
        self.assertEqual(Filepath.get_retrosheet_folder(folder='unzipped'), 
            self.rootDir + '/datasets/retrosheet/unzipped')
        self.assertEqual(Filepath.get_retrosheet_folder(folder='persistent'), 
            self.rootDir + '/datasets/retrosheet/persistent')

        # test events subfolder
        self.assertEqual(Filepath.get_retrosheet_folder(folder='unzipped', 
            subFolder='events', year=2010), self.rootDir + \
            "/datasets/retrosheet/unzipped/events2010")

        # test gamelog subfolder
        self.assertEqual(Filepath.get_retrosheet_folder(folder='unzipped', 
            subFolder='gamelog', year=2006), self.rootDir + \
            "/datasets/retrosheet/unzipped/Gamelog2006")

        # test bad request
        self.assertRaises(BadFilepathException, Filepath.get_retrosheet_folder, 
            folder='zipped', subFolder='gamelog', year=2009)

    def test_get_retrosheet_file(self):
        # test zipped and unzipped gamelog files
        self.assertEqual(Filepath.get_retrosheet_file(folder='zipped', 
            fileF='gamelog', year=2010), self.rootDir + \
            '/datasets/retrosheet/zipped/Gamelog2010.zip')
        self.assertEqual(Filepath.get_retrosheet_file(folder='unzipped', 
            fileF='gamelog', year=2012), self.rootDir + \
            '/datasets/retrosheet/unzipped/Gamelog2012/GL2012.TXT')

        # test zipped event files and unzipped boxscore files
        self.assertEqual(Filepath.get_retrosheet_file(folder='zipped', 
            fileF='event', year=2009), self.rootDir + \
            '/datasets/retrosheet/zipped/r2009events.zip')
        self.assertEqual(Filepath.get_retrosheet_file(folder='unzipped', 
            fileF='boxscore', year=2007, team='HOU'), self.rootDir + \
            "/datasets/retrosheet/unzipped/events2007/2007HOUB.txt")

        # test retrosheet id file
        self.assertEqual(Filepath.get_retrosheet_file(folder='base', 
            fileF='id'), self.rootDir + '/datasets/retrosheet/rId.txt')

        # test retrosheet batAve file
        self.assertEqual(Filepath.get_retrosheet_file(folder='persistent', 
            fileF='batAve', year=2005), self.rootDir + \
            '/datasets/retrosheet/persistent/battingAverages2005.csv')

    def test_get_lahman_file(self):
        # test master.csv
        self.assertEqual(Filepath.get_lahman_file("master"), 
            self.rootDir + '/datasets/lahman/unzipped/lahman2013-csv/Master.csv')

    def test_get_results_folder(self):
        # test in non-testing environment
        self.assertEqual(Filepath.get_results_folder(2005), 
            self.rootDir + '/results/2005')
        # test for testing environment
        self.assertEqual(Filepath.get_results_folder(2005, test=True), 
            self.rootDir + '/tests/results/2005')

    def test_results_file(self):
        # test in non-testing environment (and method 2)
        self.assertEqual(Filepath.get_results_file(
            simYear=2010, batAveYear=2009, N=50, P=10, 
            startDate=date(2010, 4, 4), endDate=date(2010, 9, 30), 
            minPA=500, minERA=None, selectionMethodNumber=2, 
            doubleDown=True), self.rootDir + "/results/2010/Sim2010," + \
            "batAve2009,N50,P10,4.4-9.30,mPA=500,sM=2,dDown=True.xlsx")

        # test for testing environment (and method 1)
        self.assertEqual(Filepath.get_results_file(
            simYear=2010, batAveYear=2009, N=50, P=10, 
            startDate=date(2010, 4, 4), endDate=date(2010, 9, 30), 
            minPA=200, minERA=None, selectionMethodNumber=1, 
            doubleDown=False, test=True), self.rootDir + "/tests/results" + \
            "/2010/Sim2010,batAve2009,N50,P10,4.4-9.30,mPA=200,sM=1,dDown=False.xlsx")

        # test for methods 3 and 4
        self.assertEqual(Filepath.get_results_file(
            simYear=2010, batAveYear=2008, N=30, P=10, 
            startDate=date(2010, 7, 7), endDate=date(2010, 10, 1), 
            minPA=400, minERA=3.7, selectionMethodNumber=3, 
            doubleDown=True),  self.rootDir + "/results/2010/Sim2010," + \
            "batAve2008,N30,P10,7.7-10.1,mPA=400,sM=3(3.7),dDown=True.xlsx")

        self.assertEqual(Filepath.get_results_file(
            simYear=2010, batAveYear=2008, N=30, P=10, 
            startDate=date(2010, 7, 7), endDate=date(2010, 10, 1), 
            minPA=400, minERA=2.1, selectionMethodNumber=4, 
            doubleDown=True),  self.rootDir + "/results/2010/Sim2010,bat" +\
           "Ave2008,N30,P10,7.7-10.1,mPA=400,sM=4(2.1),dDown=True.xlsx")

    def test_get_player_hit_info_csv_file(self):
        self.assertEqual(Filepath.get_player_hit_info_csv_file("mahompa01", 2002), 
                         self.rootDir + "/datasets/playerInfo/2002/mahompa01.txt")

    def test_get_mass_results_file(self):
        # test for non-testing environment (and method 1)
        self.assertEqual(Filepath.get_mass_results_file(
            simYearRange=(2009, 2010), sMBRange=(0, 3), 
            NRange=(1, 100), PRange=(1, 100), minPARange=(480, 502),
            minERARange=None, method=1), self.rootDir + '/results/mass/' + \
            'S2009-2010,SMB0-3,N1-100,P1-100,mPA480-502,sM=1.xlsx')

        # test for testing environment (and method 2)
        self.assertEqual(Filepath.get_mass_results_file(
            simYearRange=(2009, 2010), sMBRange=(0, 3), 
            NRange=(1, 100), PRange=(1, 100), minPARange=(480, 502), 
            minERARange=None, method=2, test=True), self.rootDir + \
            '/tests/results/mass/S2009-2010,SMB0-3,N1-100,P1-100' + \
            ',mPA480-502,sM=2.xlsx')

        # test for methods 3 and 4
        self.assertEqual(Filepath.get_mass_results_file(
            simYearRange=(2009, 2010), sMBRange=(1, 2), 
            NRange=(57, 100), PRange=(1, 3), minPARange=(100, 502), 
            minERARange=(1.0,2.5), method=3), self.rootDir + \
            '/results/mass/S2009-2010,SMB1-2,N57-100,P1-3' + \
            ',mPA100-502,sM=3(1.0-2.5).xlsx')

        self.assertEqual(Filepath.get_mass_results_file(
            simYearRange=(2008, 2008), sMBRange=(1,1), 
            NRange=(1, 100), PRange=(1, 100), minPARange=(480, 502), 
            minERARange=(5.7,9.0), method=4), self.rootDir + \
            '/results/mass/S2008-2008,SMB1-1,N1-100,P1-100' + \
            ',mPA480-502,sM=4(5.7-9.0).xlsx')
