import os
import shutil

from data import Data

class Utilities(object):
    """
    A container class for commonly used generic
    utility functions
    """
    
    @classmethod
    def convert_date(self, date):
        """
        date(year, month, day) -> string
        date: date(year, month, day) | a date of the year
        
        Produces date in retrosheet gamelog format "yyyymmdd""
        """
        return date.isoformat().replace('-', '')

    @classmethod
    def clean_retrosheet_files(self):
        """
        deletes all zipped and unzipped event and gamelog (retrosheet) files
        """
        # Clean out zipped file folder afterwards
        zippedFileFolder = Data.get_retrosheet_zipped_folder_path()
        os.chdir(zippedFileFolder)
        for file in os.listdir(os.getcwd()): 
          if os.path.isdir(file): 
            shutil.rmtree(file)
          else: 
            os.remove(file) 

        # Clean out unzipped file folder as well
        unzippedFileFolder = Data.get_retrosheet_unzipped_folder_path()
        os.chdir(unzippedFileFolder)
        for file in os.listdir(os.getcwd()): 
          if os.path.isdir(file): 
            shutil.rmtree(file)
          else: 
            os.remove(file) 
