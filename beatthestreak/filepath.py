import os

from datetime import date

from exception import BadFilepathException
from config import rootDir

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
    
    ## Make sure the commonly-missing retrosheet folder is available
    retrosheetZipped = rootDir + '/datasets/retrosheet/zipped'
    if not os.path.isdir(retrosheetZipped):
        os.mkdir(retrosheetZipped)

    @classmethod
    def get_root(self):
        # had to hard code this because using inspect.stack()[0][1] and 
        # importing beatthestreak caused all sorts of errors. 
        return rootDir

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
        if folder == 'base':
            if fileF == 'id':
                return self.get_retrosheet_folder(folder=folder) + \
                    "/rId.txt"

        if folder == 'zipped':
            if fileF == 'gamelog':
                return self.get_retrosheet_folder(folder=folder) + \
                    '/Gamelog' + str(year) + ".zip"
            if fileF == 'event':
                return self.get_retrosheet_folder(folder='zipped') + \
                    "/r" + str(year) + "events.zip"

        if folder == 'unzipped':
            if fileF == 'gamelog':
                return self.get_retrosheet_folder(folder=folder, 
                    subFolder='gamelog', year=year) + '/GL' + str(year) + '.TXT'
            if fileF == 'boxscore':
                return self.get_retrosheet_folder(folder='unzipped', 
                    subFolder='events', year = year) + "/" + str(year) + \
                    team + "B.txt"

        if folder == 'persistent':
            if fileF == 'batAve':
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
        return self.get_datasets() + "/lahman/unzipped/lahman2013-csv/" + \
                  fileF.capitalize() + ".csv"

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
    def get_results_file(self, **kwargs):
        """
        int int int int date date bool -> string
        simYear: int | year of simulation
        batAveYear: int | year with respect to which batting averages are calculated
        N: int | number of bots
        P: int | number of top players
        startDate: date | start date of simulation
        endDate: date | end date of simulation
        minPA: int | minimum number of plate appearances
        minERA: float|None | min ERA opposing pitcher needs to have for player 
           to qualify (only relevant if method in (3, 4))
        selectionMethodNumber: int | selection method number. 
            Reference: PlayerChoiceMethods.txt
        doubleDown: bool | indicates whether or not doubleDown was used
        test: bool | indicates whether or not this is being run under a test
           environment

        Produces the filepath of the results file containing the simulation with
        simYear, batAveYear, N, P, startDate, endDate
        """
        simYear = kwargs['simYear']; batAveYear = kwargs['batAveYear']
        N = kwargs['N']; P = kwargs['P']
        startDate = kwargs['startDate']; endDate = kwargs['endDate']
        minPA = kwargs['minPA']; minERA = kwargs['minERA']
        selectionMethodNumber = kwargs['selectionMethodNumber']
        doubleDown = kwargs['doubleDown']
        test = False
        if 'test' in kwargs.keys():
            test = kwargs['test']

        # if method is 3 or 4, we report minERA along with method number
        if selectionMethodNumber in (1,2):
            assert not minERA
            methodData = selectionMethodNumber
        elif selectionMethodNumber in (3,4):
            assert minERA
            methodData = "{}({})".format(selectionMethodNumber, minERA)
        else:
            raise ValueError("method number {} not valid!\n".format(
                             selectionMethodNumber))

        return self.get_results_folder(simYear, test=test) + '/Sim' + \
            str(simYear) + "," + 'batAve' + str(batAveYear) + "," + "N" + \
            str(N) + "," + "P" + str(P) + "," + str(startDate.month) + "." + \
            str(startDate.day) + "-" + str(endDate.month) + "." + \
            str(endDate.day) + "," + "mPA=" + str(minPA) + ',' + 'sM=' + \
            str(methodData) + ",dDown=" + str(doubleDown) + ".xlsx"

    @classmethod
    def get_mass_results_file(self, **kwargs):
        """
        tupleOfInts tupleOfInts tupleOfInts tupleOfInts tupleOfInts bool -> string

        simYearRange: TupleOfInts | (lowest_sim_year, highest_sim_year)
        simMinBatRange: TupleOfInts | (lowest simYear-batAveYear, highest simYear-batAveYear)
        NRange: TupleOfInts | (lowest N, highest N)
        PRange: TupleOfInts | (lowest P, highset P)
        minPARange: TupleOfInts | (lowest minPA, highest minPA)
        minERARange: TupleOfFloats | (lowest minERA, highest minERA)
        method: int | indicates which sim method we are using
        Test: bool | Indicates whether or not this is for testing purposes

        Produces the filepath for the results file for the mass simulation
        with the given parameters
        """
        simYearRange = kwargs['simYearRange']
        simMinBatRange = kwargs['sMBRange']
        NRange = kwargs['NRange']
        PRange = kwargs['PRange']
        minPARange = kwargs['minPARange']
        minERARange = kwargs['minERARange']
        method = kwargs['method']
        test = False
        if 'test' in kwargs.keys():
            test = kwargs['test']

        ## Edit root directory if it's a test run
        if test:
            results = self.get_root() +'/tests/results'
        else:
            results = self.get_root() + '/results'

        ## make sure the needed results folder is there
        if not os.path.isdir(results + '/mass'): # pragma: no cover
            os.mkdir(results + '/mass')

        if method in (1,2):
            assert not minERARange
            methodData = method
        elif method in (3,4):
            assert minERARange
            methodData = "{}({}-{})".format( method, minERARange[0], 
                                             minERARange[1])
        else:
            raise ValueError("method number {} not valid!\n".format(
                             method))

        return results + '/mass' + '/S{0}-{1}'.format(simYearRange[0], 
            simYearRange[1]) + ',' + 'SMB{0}-{1}'.format(simMinBatRange[0], 
            simMinBatRange[1]) + ',' + 'N{0}-{1}'.format(NRange[0], 
            NRange[1]) + ',' + 'P{0}-{1},'.format(PRange[0], 
            PRange[1]) + 'mPA{0}-{1},'.format(minPARange[0], 
            minPARange[1]) + 'sM={}'.format(methodData) + '.xlsx'

    @classmethod
    def get_player_hit_info_csv_file(self, lahmanID, year):
        """
        string int -> string
        lahmanID: str | lahmanID of the player of interest
        year: int | year of interest

        Returns the pathname for the player_hit_info_csv_file of the player with
        lahmanID in year year 
        """
        folder = self.get_datasets() + '/playerInfo/{0}'.format(year)
        if not os.path.isdir(folder): # pragma: no cover
            os.mkdir(folder)
        return folder + '/{0}.txt'.format(lahmanID)
