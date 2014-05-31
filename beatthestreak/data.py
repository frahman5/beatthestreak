class Data(object):
    """
    Holds relevant data that is central to multiple objects

    Purpose: single source of truth
    """
    rootDir = '/Users/faiyamrahman/programming/Python/beatthestreak' + \
        '/beatthestreak'
    retrosheetZippedFolder = '/datasets/retrosheet/zipped'
    retrosheetUnzippedFolder = '/datasets/retrosheet/unzipped'

    @classmethod
    def get_retrosheet_unzipped_folder_path(self):
        """
        None -> string

        Produces the filepath of the retrosheet unzipped files folder
        """
        return self.rootDir + self.retrosheetUnzippedFolder

    @classmethod
    def get_retrosheet_zipped_folder_path(self):
        """
        None -> string

        Produces the filepath of the retrosheet zipped files folder
        """
        return self.rootDir + self.retrosheetZippedFolder

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
        return self.get_retrosheet_unzipped_folder_path() + "/Gamelog" + str(year)

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
        return self.get_retrosheet_unzipped_folder_path() + "/events" + str(year)

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