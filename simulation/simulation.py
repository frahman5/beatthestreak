from retrosheet import Retrosheet
from utilities import Utilities

class Simulation(object)
    """
    A simulation of a beat the streak strategy over a given
    number of days
        Data:
            Leaderboard: List of highest performing bots
            Year: MLB Season (YYYY) in which to run the simulation
    """
    def __init__(self, year):
    	"""
    	int -> None
        year: 4 digit it indicating which season to run the simulation
        """
        self.year = year
        self.leaderboard = []

    def initalize(self):
    	"""
    	None -> None
    	Downloads and parse necessary retrosheet data for the simulation
    	"""
        retro = Retrosheet(self.year)
        retro.download_and_unzip(type='event')
        retrio.download_and_unzip(type='gamelog')
        retro.gen_boxscores()
        retro.clean_used_files()

    def close(self):
    	"""
    	None -> None
    	Deletes residual files from the simulation
    	"""
    	Utilities.clean_all_files()

    def set_year(self, year):
    	self.year = year

    def get_year(self):
    	return self.year

    def get_leaderboard(self):
    	return self.leaderboard

