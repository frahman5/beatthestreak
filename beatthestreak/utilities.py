import os
import shutil
import datetime

from retrosheet import Retrosheet
from filepath import Filepath

class Utilities(object):
    """
    A container class for commonly used generic utility functions
    """
    
    @classmethod
    def convert_date(self, date):
        """
        date -> string
        date:  | a date of the year
        
        Produces date in retrosheet gamelog format "yyyymmdd""
        """
        assert type(date) == datetime.date

        return date.isoformat().replace('-', '')

    @classmethod
    def clean_retrosheet_files(self):
        """
        deletes all zipped and unzipped event and gamelog (retrosheet) files.
        Leaves files in the persistent folder alone
        """
        # Get zipped and unzipped folder names
        zippedFileFolder = Filepath.get_retrosheet_folder(folder='zipped')
        unzippedFileFolder = Filepath.get_retrosheet_folder(folder='unzipped')

        # Clean out all files in both folders
        for folder in (zippedFileFolder, unzippedFileFolder):
            os.chdir(folder)
            for file in os.listdir(os.getcwd()): 
              if os.path.isdir(file): 
                shutil.rmtree(file)
              else: 
                os.remove(file) 

    @classmethod
    def ensure_gamelog_files_exist(self, year):
        """
        int -> None
        year: int | year of interest

        Checks if gamelog files for year year are on drive. If not, 
        downloads them
        """
        assert type(year) == int

        if not os.path.isfile(Filepath.get_retrosheet_file(folder='unzipped', 
            fileF='gamelog', year=year)):
            Retrosheet(year).download_and_unzip(typeT='gamelog')

    @classmethod
    def ensure_boxscore_files_exist(self, year, team):
        """
        int string -> None
        year: int | year of interest
        team: str | three letter abbreviation representing team of interest

        Checks if boxscore files for year year are on drive. If not, 
        generates them
        """
        assert type(year) == int
        assert type(team) == str

        if not os.path.isfile(Filepath.get_retrosheet_file(folder='unzipped',
            fileF='boxscore', year=year, team=team)):
            Retrosheet(year).gen_boxscores()
