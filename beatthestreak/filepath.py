import os

import beatthestreak

from utilities import Utilities

class Filepath(object):
    """
    Container for functions that return necessary file and folder paths
    """
    retrosheetZippedFolder = '/datasets/retrosheet/zipped'
    retrosheetUnzippedFolder = '/datasets/retrosheet/unzipped'

    @classmethod
    def get_root(self):
        return os.path.dirname(beatthestreak.__file__)

    @classmethod
    def get_datasets(self):
        return self.get_root() + "/datasets"
    
    @classmethod
    def get_retrosheet_folder(self, folder='base'):
        """
        string -> string
        folder : string | which retrosheet folder you want
           folder is one of ('base', 'zipped', 'unzipped', 'persistent')

        Returns filepath for the specified retrosheet folder
        """
        Utilities.type_check(folder, str)
        assert folder in ('base', 'zipped', 'unzipped', 'persistent')

        if folder == 'base':
            return self.get_datasets() + '/retrosheet'
        else:
            return self.get_datasets() + '/retrosheet/{0}'.format(folder)

    @classmethod
    def get_persistent_bat_ave_file(self, year):
        """
        int -> string

        Produces the filepath of the file containing all batting 
        averages in year year in sorted order, with associated
        lahmanIDs
        """
        assert type(year) == int and year > 1900
        return self.get_retrosheet_persistent_folder() + \
            '/battingAverages' + str(year) + '.csv'

    @classmethod
    def get_zipped_gamelog_path(self, year):
        """
        int -> string
        year: the year for which the user wants the zipped gamelog file

        Produces the filepath of the gamelog.zip for year year
        """
        return self.get_retrosheet_zipped_folder_path() + "/rGamelog" + \
            str(year) + ".zip"

    @classmethod
    def get_unzipped_gamelog_path(self, year):
        """
        int -> string
        year: the year for which the user wants the gamelog filepath

        Produces the filepath of the gamelog for year year
        """
        return self.rootDir + self.retrosheetUnzippedFolder + '/gamelog' + \
                  str(year) + "/GL" + str(year) + ".TXT"

    @classmethod
    def get_unzipped_gamelog_folder_path(self, year):
        """
        int -> string
        year : the year of interest

        Produces the path of the gamelog folder for year year
        """
        return self.get_retrosheet_folder(folder='unzipped')() + "/Gamelog" + str(year)

    @classmethod
    def get_zipped_event_files_path(self, year):
        """
        int -> string
        year: the year for which the user wants the event files get_gamelog_path

        Produces the filepath of the zipped event files for year year
        """
        return self.get_retrosheet_zipped_folder_path() + "/r" + str(year) + "events.zip" 

    @classmethod
    def get_unzipped_event_files_path(self, year):
        """
        int -> string
        year: the year for which the user wants the events filepath

        Produces the filepath of the event files directory for year year
        """
        return self.get_retrosheet_folder(folder='unzipped')() + "/events" + str(year)

    @classmethod
    def get_boxscore_file_path(self, year, team):
        """
        int string -> string
        year : the year of interest
        team: the team of interest

        Produces the filepath of the boxscore file for team team in year year
        """
        return self.get_unzipped_event_files_path(year) + "/" + str(year) + \
                      team + "B.txt"
    
    @classmethod
    def get_retrosheet_id_path(self):
        """
        None -> string

        Produces the filepath of the retrosheet ids filepath
        """
        return self.rootDir + '/datasets/retrosheet/rId.txt'

    @classmethod
    def get_lahman_path(self, file):
        """
        string -> string
        file: string name of csv file wanted. E.g: master, batting, pitching, etc
        Produces the filepath of the lahman csv corresponding to string
        """
        return self.rootDir + "/datasets/lahman/unzipped/lahman2013-csv/" + \
                  file + ".csv"

    @classmethod
    def get_results_folder(self,year):
        """
        int -> string
        year: the year for which you want the results folder

        Produces the filepath of the results folder containing simulations
        for year year
        """
        # check results folder for year year is there
        os.chdir(self.get_root_dir())
        folder = os.getcwd() + '/results/' + str(year)
        if not os.path.isdir(folder):
            os.mkdir(folder)

        return folder


    @classmethod
    def get_results_path(self, simYear, batAveYear, N, P, startDate, endDate):
        """
        int int int int date date -> string
        simYear: year of simulation
        batAveYear: year with respect to which batting averages are calculated
        N: number of bots
        P: number of top players
        startDate: start date of simulation
        endDate: end date of simulation

        Produces the filepath of the results file containing the simulation with
        simYear, batAveYear, N, P, startDate, endDate
        """
        return self.get_results_folder(simYear) + '/Sim' + str(simYear) + "," +\
            "N" + str(N) + "," + "P" + str(P) + "," + str(startDate.month) + \
            "." + str(startDate.day) + "-" + str(endDate.month) + "." + \
            str(endDate.day) + ".xlsx"

    @classmethod
    def get_mass_results_path(self, simYearRange, simMinBatRange, NRange, PRange):
        """
        tupleOfInts tupleOfInts tupleOfInts tupleOfInts -> string

        simYearRange: (lowest_sim_year, highest_sim_year)
        simMinBatRange: (lowest simYear-batAveYear, highest simYear-batAveYear)
        NRange: (lowest N, highest N)
        PRange: (lowest P, highset P)

        Produces the filepath for the results file for the mass simulation
        with the given parameters
        """
        results = self.get_results_path()
        if not os.path.isdir(results + '/mass'):
            os.mkdir(results + '/mass')

        return results + '/mass' + '/S{0}-{1}'.format(simYearRange[0], 
            simYearRange[1]) + ',' + 'SMB{0}-{1}'.format(simMinBatRange[0], 
            simMinBatRange[1]) + ',' + 'N{0}-{1}'.format(NRange[0], 
            NRange[1]) + ',' + 'P{0}-{1}'.format(PRange[0], PRange[1]) + '.xlsx'
