from retrosheet import Retrosheet
from utilities import Utilities
from researcher import Researcher

class Simulation(object):
    """
    A simulation of a beat the streak strategy over a given
    number of days
        Data:
            Leaderboard: List of highest performing bots
            Year: MLB Season (YYYY) in which to run the simulation
    """
    def __init__(self, year, startDate='default'):
    	"""
    	int -> None
        year: 4 digit int indicating in which season to run the simulation
        """
        self.year = year
        self.leaderboard = []
        if startDate == 'default':
            self.date = Researcher.get_opening_day(year)

    def setup(self):
    	"""
    	None -> None
    	Downloads and parses necessary retrosheet data for the simulation
    	"""
        retro = Retrosheet(self.year)
        retro.download_and_unzip(type='event')
        retro.download_and_unzip(type='gamelog')
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

