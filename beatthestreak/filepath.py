import os
import inspect

from datetime import date

from exception import BadFilepathException

class Filepath(object):
    """
    Container for functions that return necessary file and folder paths
    """
    retrosheetFolders = ('base', 'zipped', 'unzipped', 'persistent')
    retrosheetSubfolders = ('events', 'gamelog')
    retrosheetFiles = ('gamelog', 'event', 'boxscore', 'id', 'batAve')
    lahmanFiles = (
        'AllstarFull', 'Appearances', 'AwardsManagers', 'AwardsPlayers', 
        'AwardsShareManagers', 'AwardsSharePlayers', 'Batting', 'BattingPost', 
        'Fielding', 'FieldingOF', 'FieldingPost', 'HallOfFame', 'Managers',
        'ManagersHalf', 'Master', 'Pitching', 'PitchingPost', 'Salaries', 
        'Schools', 'SchoolsPlayers', 'SeriesPost', 'Teams', 'TeamsFranchises', 
        'TeamsHalf')

    @classmethod
    def get_root(self):
        # inspect.stack()[0] is the last item to be placed on the stack, 
        # which is the thing that called get_root. Since Filepath calls get_root,
        #, inspect.stack[0][1] returns the path of filepath.py
        return os.path.dirname(os.path.abspath(inspect.stack()[0][1]))

    @classmethod
    def get_datasets(self):
        return self.get_root() + "/datasets"
    
    @classmethod
    def get_retrosheet_folder(self, folder='base', subFolder=None, year=None):
        """
        string -> string
        folder : string | which retrosheet folder you want
           folder is one of folders in self.retrosheetFolders
        subFolder: None| String | which retrosheet subfolder you want
           subfolder is one of folders in self.retrosheetSubfolders
        year: None|int | which year, if necessary, for the folder you want


        Returns filepath for the specified retrosheet folder
        """
        assert type(folder) == str
        assert folder in self.retrosheetFolders
        if subFolder:
            assert subFolder in self.retrosheetSubfolders
            assert year
            assert type(year) == int

        if folder == 'base':
            return self.get_datasets() + '/retrosheet'
        if folder == 'unzipped' and subFolder: 
            if subFolder == 'events':
                return self.get_datasets() + \
                    '/retrosheet/unzipped/events' + str(year)
            if subFolder == 'gamelog':
                return self.get_datasets() + \
                    '/retrosheet/unzipped/Gamelog' + str(year)
        if (not subFolder) and (not year):
            return self.get_datasets() + '/retrosheet/{0}'.format(folder)

        raise BadFilepathException("Not valid. folder: {0}.".format(
            folder) + "subFolder: {0}.Year: {1}".format(subFolder, year))

    @classmethod
    def get_retrosheet_file(self, folder, fileF, year=None, team=None):
        """
        string string None|year-> string

        folder: string | retrosheet folder in while file resides
             folder is one of folders in self.retrosheetFolders
        file: string | type of file desired
             file is one of files in self.retrosheetFiles
        year: None|Int | If necessary, specifies the year for the file
             path desired
        team: None|Str | If necessary, specifies the team for the file

        Returns filepath for the specified retrosheet file
        """
        assert type(folder) == str
        assert type(fileF) == str
        if team:
            assert type(team) == str
        if year:
            assert type(year) == int
        assert folder in self.retrosheetFolders
        assert fileF in self.retrosheetFiles

        if folder == 'base':
            if fileF == 'id':
                return self.get_retrosheet_folder(folder=folder) + \
                    "/rId.txt"

        if folder == 'zipped':
            if fileF == 'gamelog':
                assert year
                return self.get_retrosheet_folder(folder=folder) + \
                    '/Gamelog' + str(year) + ".zip"
            if fileF == 'event':
                assert year
                return self.get_retrosheet_folder(folder='zipped') + \
                    "/r" + str(year) + "events.zip"

        if folder == 'unzipped':
            if fileF == 'gamelog':
                assert year
                return self.get_retrosheet_folder(folder=folder, 
                    subFolder='gamelog', year=year) + '/GL' + str(year) + '.TXT'
            if fileF == 'boxscore':
                assert year
                assert team
                return self.get_retrosheet_folder(folder='unzipped', 
                    subFolder='events', year = year) + "/" + str(year) + \
                    team + "B.txt"

        if folder == 'persistent':
            if fileF == 'batAve':
                assert year
                return self.get_retrosheet_folder(folder='persistent') + \
                    '/battingAverages' + str(year) + '.csv'
        

        raise BadFilepathException("Not valid. folder: {0}.".format( # pragma: no cover
            folder) + "fileF: {0}.Year: {1}.Team: {2}".format(fileF, year, team))

    @classmethod
    def get_lahman_file(self, fileF):
        """
        string -> string

        fileF: string name of csv file wanted. 
           fileF must be self.lahmanFiles

        Returns the filepath of the lahman csv corresponding to fileF
        """
        assert type(fileF) == str
        assert fileF.lower() in [string.lower() for string in self.lahmanFiles]

        return self.get_datasets() + "/lahman/unzipped/lahman2013-csv/" + \
                  fileF + ".csv"

    @classmethod
    def get_results_folder(self,year, test=False):
        """
        int bool -> string
        year: int | the year for which you want the results folder
        test: bool | indicates whether or not this is being run 
           from a test environment

        Returnsthe filepath of the results folder containing simulations
        for year year
        """
        assert type(year) == int

        # check results folder for year year is there
        os.chdir(self.get_root())

        if test: # if its a test case, get the test results folder
            folder = os.getcwd() + '/tests/results/' + str(year)
        else: # otherwise get the production results folder
            folder = os.getcwd() + '/results/' + str(year)
        if not os.path.isdir(folder): # pragma: no cover
            os.mkdir(folder)

        return folder

    @classmethod
    def get_results_file(self, simYear, batAveYear, N, P, startDate, endDate, 
           test=False):
        """
        int int int int date date bool -> string
        simYear: int | year of simulation
        batAveYear: int | year with respect to which batting averages are calculated
        N: int | number of bots
        P: int | number of top players
        startDate: date | start date of simulation
        endDate: date | end date of simulation
        test: bool | indicates whether or not this is being run under a test
           environment

        Produces the filepath of the results file containing the simulation with
        simYear, batAveYear, N, P, startDate, endDate
        """
        for param in (simYear, batAveYear, N, P):
            assert type(param) == int
        assert type(startDate) == date
        assert type(endDate) == date

        return self.get_results_folder(simYear, test=test) + '/Sim' + \
            str(simYear) + "," + 'batAve' + str(batAveYear) + "," + "N" + \
            str(N) + "," + "P" + str(P) + "," + str(startDate.month) + "." + \
            str(startDate.day) + "-" + str(endDate.month) + "." + \
            str(endDate.day) + ".xlsx"

    @classmethod
    def get_mass_results_file(self, simYearRange, simMinBatRange, NRange, PRange, 
            test=False):
        """
        tupleOfInts tupleOfInts tupleOfInts tupleOfInts bool -> string

        simYearRange: TupleOfInts | (lowest_sim_year, highest_sim_year)
        simMinBatRange: TupleOfInts | (lowest simYear-batAveYear, highest simYear-batAveYear)
        NRange: TupleOfInts | (lowest N, highest N)
        PRange: TupleOfInts | (lowest P, highset P)
        Test: bool | Indicates whether or not this is for testing purposes

        Produces the filepath for the results file for the mass simulation
        with the given parameters
        """
        for param in (simYearRange, simMinBatRange, NRange, PRange):
            assert type(param[0]) == int
            assert type(param[1]) == int
            assert len(param) == 2
        
        if test:
            results = self.get_root() +'/tests/results'
        else:
            results = self.get_root() + '/results'
        if not os.path.isdir(results + '/mass'): # pragma: no cover
            os.mkdir(results + '/mass')

        return results + '/mass' + '/S{0}-{1}'.format(simYearRange[0], 
            simYearRange[1]) + ',' + 'SMB{0}-{1}'.format(simMinBatRange[0], 
            simMinBatRange[1]) + ',' + 'N{0}-{1}'.format(NRange[0], 
            NRange[1]) + ',' + 'P{0}-{1}'.format(PRange[0], PRange[1]) + '.xlsx'

