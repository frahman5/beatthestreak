import unittest

from datetime import date

from beatthestreak.filepath import Filepath
from beatthestreak.tests import setup, teardown
from beatthestreak.exception import BadFilepathException

class TestFilepath(unittest.TestCase):
    """
    As these tests use filepaths native to the development
    machine, they only work on the development machine
    """

    def setUp(self):
        self.rootDir = '/Users/faiyamrahman/programming/Python/beatthestreak' + \
        '/beatthestreak'
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

        # # test bad file path exception
        # self.assertRaises(BadFilepathException, Filepath.get_retrosheet_file,
        # folder='persistent', fileF='omega', year=2002)

    def test_get_lahman_file(self):
        # test master.csv
        self.assertEqual(Filepath.get_lahman_file("master"), 
            self.rootDir + '/datasets/lahman/unzipped/lahman2013-csv/master.csv')

    def test_get_results_folder(self):
        self.assertEqual(Filepath.get_results_folder(2005), 
            self.rootDir + '/results/2005')

    def test_results_file(self):
        self.assertEqual(Filepath.get_results_file(2010, 2009, 50, 10, 
            date(2010, 4, 4), date(2010, 9, 30)), self.rootDir + \
            "/results/2010/Sim2010,batAve2009,N50,P10,4.4-9.30.xlsx")

    def test_get_mass_results_file(self):
        self.assertEqual(Filepath.get_mass_results_file((2009, 2010), (0, 3), 
            (1, 100), (1, 100)), self.rootDir + '/results/mass/S2009-2010' + \
        ',SMB0-3,N1-100,P1-100.xlsx')